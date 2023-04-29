import cv2
import numpy as np
from flask import Flask, render_template, Response
import os
import json

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