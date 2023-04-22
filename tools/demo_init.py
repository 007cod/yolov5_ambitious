from distutils.log import log
from tkinter.messagebox import NO
from flask import Flask, render_template, Response,jsonify
import time
import cv2 as cv
import matplotlib
import json
import copy

from ASC import select
from flask_tools import gen_frames, Store, app
from tools.datatools import *
from tools.data_init import *
from tools.cap import get_cap
from tools.model import get_model
from Person_O import save_info,Person
matplotlib.use('Agg')

class demo():
    def __init__(self) -> None:
        #数据库初始化
        self.app = app
        self.db = db
        self.db.app = app
        self.db.init_app(app)
        '''加载配置文件'''
        self.config_path = './config.json' 
        self.save_img_path = "./static/images/PersonImg"
        self.store = Store()
        self.q = [0, Person(1,'b', 'kunkun'), 10, 10, Person(2, 'a', 'lanqiu'), 20]  #[进入时间，人物信息，离开时间]
        self.init_config()

    def init_config(self):
        self.q = [0, Person(1,'b', 'kunkun'), 10, 10, Person(2, 'a', 'lanqiu'), 20]  #[进入时间，人物信息，离开时间]
        self.state = ""
        self.label = ""
        self.person = None
        for id in range(len(self.q)):
            if isinstance(self.q[id], int):
                self.q[id] = time.time() + self.q[id]
        with open(self.config_path,'r',encoding='utf-8') as f: 
            self.arg = json.load(f)
        """--------------初始化分拣模型-----------------------------"""
        self.sec = select(get_model(self.arg), self.arg, threshold=0.5)
        self.cap = get_cap(self.arg['path'])
        """--------------初始化人物识别模型-----------------------------"""
        self.sa = save_info(self.q, self.arg['v'], self.arg['x_len'], self.save_img_path)

        # 解决第一张图片为空
        empty_img = cv.imread("empty.png")
        empty = gen_frames(empty_img)
        self.store.save_img2(empty)

    def genPic(self):
        num = 0
        time_t = time.time()
        for img in self.cap: 
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

            self.person, image = self.sa.run(img_clone)
            update_person(self.person, image)

            img, state, items = self.sec.run(img)
            self.store.set_state(state)
            # print("--------------", items[0])
            if len(items) != 0:
                img2, label = items[0]
                img2 = gen_frames(img2)
                self.store.save_img2(img2)
                self.store.set_label(label)
            img = gen_frames(img)
            yield img

