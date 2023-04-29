import time
import cv2
import matplotlib
import json
import copy
import datetime

from ASC import select
from flask_tools import gen_frames, app
from tools.datatools import add_banned_item, add_passenger, update_person
from tools.data_init import db, Prohibited_Items, Passengers
from tools.cap import get_cap
from tools.model import get_model
from Person_O import save_info,Person
matplotlib.use('Agg')


class Store():
    def __init__(self) -> None:
        self.arg = {'img' : None,
                    'x_ray_img' : None,
                    'label': "",
                    'state': "",
                    'isChange':False}

    def set_label(self, label):
        if(label != self.arg['label']):
            self.arg['isChange'] = True
        self.arg['label'] = label

    def set_state(self, state):
        if (state != self.arg['state']):
            self.arg['isChange'] = True
        self.arg['state'] = state

    def get_arg(self, name):
        while True:
            yield self.arg[name]

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
        self.init_config()

    def init_config(self):
        self.q = [0, Person(1,'b', 'kunkun'), 20, 20, Person(2, 'a', 'lanqiu'), 300]  #[进入时间，人物信息，离开时间]
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
        empty_img = cv2.imread("empty.png")
        empty = gen_frames(empty_img)
        self.store.arg['x_ray_img'] = empty

    def get_main(self):
        num = 0
        time_t = time.time()
        for img in self.cap: 
            num += 1
            if num % 3 != 0:
                continue
            lt = time.time()
            if lt-time_t < 0.20:
                time.sleep(0.20-(lt-time_t))
            time_t = time.time()

            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img_clone = copy.deepcopy(img)

            self.person, image = self.sa.run(img_clone)
            update_person(self.person, image)

            img, state, items = self.sec.run(img)
            self.store.set_state(state)
            self.store.arg['img'] = gen_frames(img)
            # print("--------------", items[0])
            if len(items) != 0:
                img2, label = items[0]
                self.store.arg['x_ray_img'] = gen_frames(img2)
                self.store.set_label(label)
                img2Bt =  cv2.imencode('.png', img2)[1].tobytes()
                if self.person:
                    with app.app_context():
                        add_banned_item(label, '重庆', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.person.name, self.person.id,img2Bt)
            yield self.store.arg['img']