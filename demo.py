from distutils.log import log
from tkinter.messagebox import NO
import cv2
from flask import Flask, render_template, Response
import imageio
import os
import numpy as np
import time
import cv2 as cv
import yaml
from ASC import select
import matplotlib
import sys
import json

from yolov5_trt import *
# from flask_socketio import SocketIO, emit

matplotlib.use('Agg')


"""----------------------------------------------------"""
""" 读取视频和模型初始化predictor """
#path = './2222.mp4'
#cap = imageio.get_reader(path, 'ffmpeg')
#cap2 = imageio.get_reader(path, 'ffmpeg')


cap = cv.VideoCapture(0)  # 视频流
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))  #读取视频格式
# 设置分辨率
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

chinese_label = ['打火机', '压力容器', '刀', '充电宝',
                 '打火机油', '手铐', '弹弓', '鞭炮', '尖锐工具', '甩棍', '电棍']

label_list = ['lighter','pressure','knife','powerbank','zippooil','handcuffs','slingshot','firecrackers','sharpTools','expandableBaton','electricBaton']




PLUGIN_LIBRARY = "build/libmyplugins.so"
engine_file_path = "build/yolov5s.engine"
if len(sys.argv) > 1:
    engine_file_path = sys.argv[1]
if len(sys.argv) > 2:
    PLUGIN_LIBRARY = sys.argv[2]

ctypes.CDLL(PLUGIN_LIBRARY)

yolov5_wrapper = YoLov5TRT(engine_file_path)
infer_model = yolov5_wrapper.infer

""" 舵机初始化 """
#kit = ServoKit(channels=16)
#kit.servo[8].angle = 0
"""安检数据"""

num = 0
times = 0
im_size = 416

"""速度，安检机实际长度， 设备到安检机的实际长度，"""
v = 73.3/5
x_len = v*2.39
dev_p = 3.32*v-x_len


"""-------------------------------------------"""


sec = select(infer_model, label_list, chinese_label,
             v, x_len, dev_p, threshold=0.5)
lt = time.time()
time_t = time.time()


def gen_frames(frame):  # generate frame by frame from camera
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result






app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key'
# socketio = SocketIO()
# socketio.init_app(app, cors_allowed_origins='*')

# name_space = '/demo'


class Store():
    def __init__(self) -> None:
        self.img2 = None
        self.label = ""
        self.state = ""
        self.ischange = False

    def save_img2(self, x):
        self.img2 = x

    def get_img2(self):
        return self.img2

    def set_label(self, label):
        if(label != self.label):
            self.ischange = True
        self.label = label

    def set_state(self, state):
        if (state != self.state):
            self.ischange = True
        self.state = state

    def get_status(self):
        res = self.label, self.state, self.ischange
        self.ischange = False
        return res


store = Store()


class pre(object):
    def __init__(self, predict1, predictor1, preprocess1, im_size1):
        self.predict = predict1
        self.im_size = im_size1
        self.preprocess = preprocess1
        self.predictor = predictor1

    def __call__(self, img):
        scale_factor = np.array([self.im_size * 1. / img.shape[0], self.im_size * 1. / img.shape[1]]).reshape((1, 2)).astype(
            np.float32)
        im_shape = np.array([self.im_size, self.im_size]
                            ).reshape((1, 2)).astype(np.float32)
        data = self.preprocess(img, self.im_size)
        result = self.predict(self.predictor, [im_shape, data, scale_factor])
        return result



state = ""
label = ""

# 解决第一张图片为空
empty_img = cv.imread("empty.png")
empty = gen_frames(empty_img)
store.save_img2(empty)
last_state = False
l_t = time.time()

def genPic():
    global state, label, num, time_t, l_t,last_state
    while cap.isOpened():
        ret,img=cap.read()
        img = img[:400, 335:, :]
        
        img, state, items = sec.run(img)
        
        if state==True and last_state==False:
            l_t = time.time()
        if state==False and time.time()-l_t<0.6:
            state = True
        img = cv2.resize(img,(330,352))
        store.set_state(state)
        #print("--------------")
        if len(items) != 0:
            
            img2, label = items[0]
            #print(img2)
            img2 = gen_frames(img2)
            store.save_img2(img2)
            store.set_label(label)
        else:
            store.set_label("")
        img = gen_frames(img)
        last_state = state
        yield img
        


def genPic2():
    while True:
        yield store.get_img2()

@app.route('/video_feed')
def video_feed():
    img = genPic()
    # print(img)
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(img, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/things')
def things():
    img2 = genPic2()
    return Response(img2, mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/state")
def get_state():
    label, state, isChange = store.get_status()
    return Response(json.dumps({"label": label, "state": state, "isChange": isChange}), mimetype='application/json')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html', message_list=state)


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
