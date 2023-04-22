import cv2
import numpy as np
from flask import Flask, render_template, Response
import os
import json

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

def gen_frames(frame):  # generate frame by frame from camera
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

config_path  = './config.json' 
with open(config_path,'r',encoding='utf-8') as f: 
    arg = json.load(f)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+ os.path.join(os.getcwd(), arg['database_path'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False