import cv2 as cv
import collections
import time
import random
import numpy as np
import colorsys
import matplotlib
import copy
from tools.draw import *
from PIL import Image, ImageDraw, ImageFont
matplotlib.use('Agg')

class select(object):
    def __init__(self, infer_model, arg, threshold=0.5):
        self.last_time = time.time()
        self.con_ti = collections.deque()
        self.start_time = time.time() #分拣开始时间
        self.end_time = self.start_time #分拣结束时间
        self.last_danger = False #上一帧的危险状态
        self.last_pixel = False  #上一帧是否在最左侧检测到物品
        self.item_len = 0 #待出物品的长度
        self.state = False #分拣机状态
        self.threshold=threshold #检测阈值
        self.dq_loc = [] #违禁品位置队列
        self.infer_model = infer_model #推理模型
        self.v = arg['v']#安检机速度
        self.x_len = arg['x_len'] #图片长度对应的真实长度
        self.dev_p = arg['dev_p'] #安检机到分拣机的距离

        self.img_shape = None
        self.label_list =arg['chinese_label']
        self.num_classes = len(arg['chinese_label'])
        self.new_loc = []
        self.new_items = []
        self.eng = arg['label_list']

    def run(self, image):
        self.img_shape = image.shape
        time_t = time.time()
        result = self.infer_model(image)
        self.get_control(image, result[0],self.state)
        self.last_time = time_t
        self.con_ti.append([self.start_time, self.end_time])
        self.control()

        colo_map = get_color_map_list(self.num_classes)
        img = draw_img(image, result[0], self.eng, colo_map, self.threshold)
        return img, self.state, self.new_items
    
    def get_img(self,frame):
        result = self.infer_model(frame)
        colo_map = get_color_map_list(self.num_classes)
        img = draw_img(frame, result[0], self.eng, colo_map, self.threshold)
        return img

    def pixel(self, image, indy):  # 判断这一列是否有物品
        mask = image[:, indy, :] < 230
        if np.sum(mask) > 0:
            return True
        sum = np.array(image[:, indy, :]).mean()
        if sum < 230:
            return True
        else:
            return False

    def get_item_size(self, image):  # 得到物品的长度
        len = 0
        for i in range(image.shape[1]):
            if self.pixel(image, i):
                len += 1
            else:
                break
        # print(len)
        return len

    def is_dangerous(self, lens):  # 判断当前是否有危险物品
        if len(self.dq_loc)!=0 and self.dq_loc[0][0] < lens: 
            return True
        else:
            return False

    def get_dan_loc(self,results,image):
        self.new_items = []
        for dt in np.array(results):
            c_id, bbox, score = dt[0], dt[2:], dt[1]
            if score < self.threshold:
                continue
            xmin, ymin, xmax, ymax = bbox
            x_loc = (xmax + xmin) / 2
            y_loc = (ymax + ymin) / 2
            flag = True
            #print(len(self.dq_loc))
            for x,y in self.dq_loc:
                if pow(x-x_loc,2)+pow(y-y_loc,2) < 10000:
                    #print(abs(pow(x-x_loc,2)+pow(y-y_loc,2)))
                    flag = False
                    break
            if flag:
                self.dq_loc.append([x_loc,y_loc])
                img = image[int(ymin):int(ymax),int(xmin):int(xmax),:]
                self.new_items.append([img,self.label_list[int(c_id)]])
        self.dq_loc.sort(key=lambda x:x[0])
        # print(len(self.new_loc))

    def update_loc(self):
        """更新危险物品的位置信息"""
        len_ration = self.x_len / self.img_shape[1]  # 实际长度与像素的比值
        d_len = (time.time() - self.last_time) * self.v / len_ration
        # print(d_len)
        self.dq_loc = [[i[0] - d_len,i[1]] for i in self.dq_loc]
        self.dq_loc.sort(key=lambda x:x[0])
        #print(len(self.dq_loc))
        if len(self.dq_loc)==0 or self.dq_loc[len(self.dq_loc)-1][0] <= 0:
            self.dq_loc = []
            return
        idxx = int(0)
        for idx, p in enumerate(self.dq_loc):
            if p[0] > 0:
                idxx = idx
                break
        self.dq_loc = self.dq_loc[idxx:]

    def get_control(self, image, results, last_state):
        """
        :param image: 图片
        :param results: 预测结果
        :param last_state: 刚出安检机的物品状态
        :param last_time 上一张图片的检测时间
        :param dq_loc:上一状态危险物品位置的列表
        :param start_time 电机开始时间
        :param end_time: 电机结束时间
        :param is_danger: 最近一个物品是否是危险物品
        :param last_pixel: 上一帧最近物品是否要出安检机的状态
        :param item_len 正在出安检机的危险品的尺寸
        :param v: 传送带速度
        :param pix_len 安检机的显示像素
        :param x_len 安检机的实际长度
        :param dev_p 设备到安检机的实际距离
        :param threshold: 阈值
        :return: 当前图片的属性 dq_loc, start_time, end_time, is_danger, is_pixel, item_len
        """
        len_ration = self.x_len / self.img_shape[1]
        self.update_loc()
        self.get_dan_loc(results, np.copy(image))

        is_pixel = self.pixel(image, 0)  # 得到最近物品是否要出安检机的状态

        if not self.last_pixel and is_pixel: #正要出安检机的行李
            '''物品正好到达安检机的边缘'''
            self.item_len = self.get_item_size(image)  # 正要出安检机的物品尺寸
            self.last_danger = self.is_dangerous(self.item_len)
            #print(now_is_danger)

        elif self.last_pixel and not is_pixel: #行李刚好完全出安检机
            """ 此时物品已经完全出安检机 """
            #print('item_len:{}'.format(self.item_len))
            if self.last_danger:
                print("danger")
                self.end_time = time.time() + self.dev_p / self.v - 0.5
                self.start_time = time.time() + (self.dev_p - self.item_len * len_ration) / self.v - 0.5
                print(self.end_time - self.start_time)
                self.last_danger = False
            else:
                print("not danger")

        elif is_pixel and not self.last_danger:
            """ 更新正要出安检机的物品的危险状态 """
            n_len = self.get_item_size(image)  # 正要出安检机的物品尺寸
            now_is_danger = self.is_dangerous(n_len)
            self.last_danger = now_is_danger

        elif self.last_danger and not is_pixel:
            self.last_danger = False

        self.last_pixel = is_pixel
        return

    def control(self):
        now_time = time.time()
        while len(self.con_ti) and self.con_ti[0][1] < now_time:
            self.con_ti.popleft()
        if len(self.con_ti) == 0:
            start_time = now_time - 1
            end_time = start_time
        else:
            start_time = self.con_ti[0][0]
            end_time = self.con_ti[0][1]
        #print(f"{now_time},{start_time},{end_time}")
        if now_time > start_time and now_time < end_time and not self.state:
            """
            如果当前时间在要求的闭合时间段，并且舵机是打开的， 则将舵机闭合
            """
            # print("on")
            # kit.servo[8].angle = 75
            self.state = True
        elif self.state and (now_time > end_time or now_time < start_time):
            """
            如果当前时间不在要求的闭合时间，并且舵机是闭合的， 则将舵机打开
            """
            # print("off")
            # kit.servo[8].angle = 0
            self.state = False

        '''可视化'''
        #im = np.zeros((336, 20, 3))
        # if self.state:
        #     #im[:, :, 2] = 255
        #     #cv.imshow('choice', im)
        #     print("on")
        # else:
        #     #im[:, :, 1] = 255
        #     #cv.imshow('choice', im)
        #     print("off")
        # return
