import numpy as np
import matplotlib 
from PIL import Image, ImageDraw, ImageFont
import cv2
import random
matplotlib.use('Agg')

def cv2AddChineseText(img, text, position, textColor=(0, 255, 0), textSize=30):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text(position, text, textColor, font=fontStyle)
    cv2.imshow('fefe', cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR))
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def Chinese_plot_box(x, image, color=None, label = None, line_thickness=None):
        """x是xyxy坐标
        label="人"等汉字"""
        cv2img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pilimg = Image.fromarray(cv2img)
        draw = ImageDraw.Draw(pilimg)  # 图片上打印
        tl = (
                line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
        )


        tl = line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
        # 颜色随机
        color = color or [random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
        # 这个是大框
        draw.rectangle([int(x[0]), int(x[1]), int(x[2]), int(x[3])], outline=(255, 0, 0),
                       fill=None, width=tl)
        if label:
            # print(label)
            tf = max(tl - 1, 1)  # font thickness  字体大小
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 6, thickness=tf)[0]
            # 衬托字体的小矩形
            # ([xyxy]，outline轮廓的颜色， fill用于填充的颜色)
            draw.rectangle([int(x[0]), int(x[1]), c1[0] + t_size[0], c1[1] - t_size[1] - 3], outline=(255, 0, 0),
                           fill=(255, 0, 0), width=1)
            # cv2.rectangle(image, c1, c2, (0,255,0), -1)  # filled
            # 这个颜色必须是数组tuple(colour)
            font = ImageFont.truetype("ziti.ttf", tl//3, encoding="utf-8")
            draw.text(((int(x[0]), int(x[1]) - 23)), label, tuple(color), font=font)
            image = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
        return image
def plot_one_box(x, img, color=None, label=None, line_thickness=None):
        """
        description: Plots one bounding box on image img,
                     this function comes from YoLov5 project.
        param:
            x:      a box likes [x1,y1,x2,y2]
            img:    a opencv image object
            color:  color to draw rectangle, such as (0,255,0)
            label:  str
            line_thickness: int
        return:
            no return

        """
        tl = (
                line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
        )  # line/font thickness
        color = color or [random.randint(0, 255) for _ in range(3)]
        c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
        cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
        if label:
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
            cv2.putText(
                img,
                label,
                (c1[0], c1[1] - 2),
                0,
                tl / 3,
                [225, 255, 255],
                thickness=tf,
                lineType=cv2.LINE_AA,
            )
        return img

def draw_img(img, results, label_list, color_map, threshold):
    for box in np.array(results):
        id = int(box[0])
        score = box[1]
        box = box[2:]
        if score < threshold:
            continue
        plot_one_box(
            box,
            img,
            color=color_map[id],
            label="{}:{:.2f}".format(
                label_list[id], score
            ),
        )

        # img = self.Chinese_plot_box(
        #     box,
        #     img,
        #     color=color_map[id],
        #     label="{}:{:.2f}".format(
        #         label_list[id], score
        #     ),
        # )
        # item = r_img[int(y1):int(y2),int(x1):int(x2),:]
        # items.append((item,label_list[id]))
        #cv.imshow('danger', img[int(y1):int(y1+y2),int(x1):int(x1+x2),:])
        #print(label_list[id])
    return img

def get_color_map_list(num_classes):
    # 为类别信息生成对应的颜色列表
    color_map = num_classes * [0, 0, 0]
    for i in range(0, num_classes):
        j = 0
        lab = i
        while lab:
            color_map[i * 3] |= (((lab >> 0) & 1) << (7 - j))
            color_map[i * 3 + 1] |= (((lab >> 1) & 1) << (7 - j))
            color_map[i * 3 + 2] |= (((lab >> 2) & 1) << (7 - j))
            j += 1
            lab >>= 3
    color_map = [color_map[i:i + 3] for i in range(0, len(color_map), 3)]
    color_map[2] = [0, 0, 128]
    color_map[4] = [0, 128, 0]
    return color_map