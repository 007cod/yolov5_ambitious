from distutils.log import log
from tkinter.messagebox import NO
import cv2
from flask import Flask, render_template, Response,jsonify
import imageio
import numpy as np
import time
import cv2 as cv
import matplotlib
import json
import copy
from PIL import Image
import base64
import datetime
import random

from ASC import select
from flask_tools import gen_frames, Store, app
from tools.datatools import *
from tools.data_init import *
from tools.model import get_model
from Person_O import save_info,Person
matplotlib.use('Agg')

#数据库初始化
db.app = app
db.init_app(app)

'''加载配置文件'''
config_path  = './config.json' 
with open(config_path,'r',encoding='utf-8') as f: 
    arg = json.load(f)
store = Store()

def get_cap(path):
    """ 读取视频和模型初始化predictor """
    if isinstance(path, str):
        cap = imageio.get_reader(path, 'ffmpeg')
    else:
        cap = cv.VideoCapture(path)  # 视频流
        cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))  #读取视频格式
        # 设置分辨率
        cap.set(cv.CAP_PROP_FRAME_WIDTH, 1024)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, 768)
    return cap

"""--------------初始化分拣模型-----------------------------"""
sec = select(get_model(arg), arg, threshold=0.5)

cap = get_cap(arg['path'])

num = 0
time_t = time.time()
q = [0, Person(1,'b', 'kunkun'), 10, 10, Person(2, 'a', 'lanqiu'), 20]  #[进入时间，人物信息，离开时间]

"""--------------初始化人物识别模型-----------------------------"""
save_img_path = "./static/images/PersonImg"
sa = save_info(q, arg['v'], arg['x_len'], save_img_path)

def gen_frames(frame):  # generate frame by frame from camera
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


state = ""
label = ""
person = None
# 解决第一张图片为空
empty_img = cv.imread("empty.png")
empty = gen_frames(empty_img)
store.save_img2(empty)

def genPic():
    global state, label, num, time_t, person
    for id in range(len(q)):
        if isinstance(q[id], int):
            q[id] = time.time() + q[id]
    print("*"*20)
    print(time_t)
    for img in cap: 
        pix_len = img.shape[1]
        num += 1
        if num % 3 != 0:
            continue
        lt = time.time()
        if lt-time_t < 0.20:
            time.sleep(0.20-(lt-time_t))
        time_t = time.time()

        img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

        img_clone = copy.deepcopy(img)

        person, image = sa.run(img_clone)
        update_person(person, image)

        img, state, items = sec.run(img)
        store.set_state(state)
        # print("--------------", items[0])
        if len(items) != 0:
            img2, label = items[0]
            img2 = gen_frames(img2)
            store.save_img2(img2)
            store.set_label(label)
        img = gen_frames(img)
        yield img


def genPic2():
    while True:
        yield store.get_img2()

@app.route('/video_feed')
def video_feed():
    img = genPic()
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
    # global state, label, num, time_t, person
    # state = ""
    # label = ""
    # person = None
    # time_t = time.time()
    # print("*"*20)
    # print(person)
    # for id in range(len(q)):
    #     if isinstance(q[id], int):
    #         q[id] = time_t + q[id]
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/<name>')
def show_person(name):
    print('-'*20 + name)
    passenger = Passengers.query.filter_by(name=name).first()
    prohibited = Prohibited_Items.query.filter_by(passenger_name = name).first()
    return render_template('user.html', passenger = passenger, prohibited = prohibited, base64=base64)

@app.route('/name')
def name():
    if person:
        return json.dumps({'name' : person.name})
    else: 
        return json.dumps({'name' : '无'})
    
@app.route('/items/<name>')
def items(name):
    passenger = Passengers.query.filter_by(name=name).first()
    items_data = base64.b64encode(passenger.Xray_image).decode()
    return json.dumps({'items_data' : items_data})

@app.route('/data')
def data():
    now = datetime.datetime.now()
    data = []
    for i in range(24):
        data.append({
            'hour': i,
            'count': random.randint(0, 100)
        })
    return jsonify({
        'timestamp': now.timestamp(),
        'data': data
    })
    
def init_data():
    with open('./static/images/kunkun.jpg','rb') as f:
        data_kunkun = f.read()
    with open('./static/images/avatar.jpeg','rb') as f:
        data_lanqiu = f.read()
    with open('static/images/unsafty/kunkun.jpg', 'rb') as f:
        last_kunkun = f.read()
    add_passenger('kunkun', 'Beijing', '123456789', '123456789012345678', 'Shanghai', 'G1234', data_kunkun,None)
    add_passenger('lanqiu', 'Beijing', '123456789', '123456789012345678', 'Shanghai', 'G1234', data_lanqiu,None)
    add_banned_item('knife', 'Chongqing', '2023-04-20 10:00:00', 'kunkun', 1, last_kunkun)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        #init_data()
        app.run(debug=False, host="0.0.0.0")
