import numpy as np
import time
import cv2 as cv
import os
class Person:
    def __init__(self, id, sex, name):
        self.id = id
        self.sex = sex
        self.name = name

class save_info():
    def __init__(self, data : Person, v : int, dl : int , path : str) -> None: #人物放行李的状态，传送带速度， 安检机长度，
        self.start_time = None  #进入时间
        self.end_time = None  #离开时间
        self.person = None   #人物信息
        self.photo  = None  #图片
        self.data_person = data  #[进入时间，人物信息，离开时间]
        self.dlt = dl/v  #物品到达安检机的所需时间
        self.pl = 5
        self.gg = True #判断物品第一次进入安检机
        self.root_path = path #图片保存路径
        
    def run(self, frame):
        self.get_data()
        nt = time.time()
        if not self.start_time or nt - self.start_time < self.dlt: #还没有放物品，或则物品还未进入安检机
            self.gg = True
        elif self.gg and self.start_time and nt - self.start_time >= self.dlt: #物品第一次进入安检机
            id = frame.shape[1] - 1
            for j in range(frame.shape[1]-1, -1, -1):
                if np.mean(np.abs(frame[:, j, :])) > 240:
                    id = j
                    break
            self.photo = frame[:, id:, :]
            self.gg = False
        elif (not self.end_time or nt - self.end_time < self.dlt) and self.photo is not None:  #还未完成放物品，或则还有物品未进入安检机
            id = frame.shape[1] - 1
            for j in range(frame.shape[1]-1, -1, -1):
                if np.mean(np.abs(frame[:, j, :] - self.photo[:, -1, :])) < 5:
                    # print("--"*20)
                    # print(np.mean(np.abs(frame[:, j, :] - self.photo[:, -1, :])))
                    id = j
                    break
            kpo = np.zeros((frame.shape[0], frame.shape[1] - id - 1 + self.photo.shape[1], 3))
            kpo[:, self.photo.shape[1]:, :] = frame[:, id + 1:, :]
            kpo[:, :self.photo.shape[1], :] = self.photo
            self.photo = kpo
        elif self.end_time and nt - self.end_time > self.dlt: #物品已经全部经过安检机的扫描
            self.save()
            self.start_time = self.end_time = self.person = self.photo = None
        return self.person, self.photo
            

    def get_data(self):
        '''
        更新数据
        '''
        if not self.start_time:
            if len(self.data_person):
                self.start_time = self.data_person[0]
                self.data_person.pop(0)
        if self.start_time:
            if not self.person and len(self.data_person) and isinstance(self.data_person[0], Person):
                self.person = self.data_person[0]
                self.data_person.pop(0)
            if not self.end_time and len(self.data_person) and isinstance(self.data_person[0], float):
                self.end_time = self.data_person[0]
                self.data_person.pop(0)

    def save(self):
        cv.imwrite(self.root_path+ f'/{self.person.name}.jpg', self.photo)
    
if __name__ == '__main__':
    pass



