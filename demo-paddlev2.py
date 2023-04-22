from flask import Flask, render_template, Response,jsonify
import matplotlib
import json
import base64
import datetime
import random
from tools.datatools import add_banned_item, add_passenger, update_person
from tools.data_init import *
from tools.demo_init import demo
matplotlib.use('Agg')

Demo = demo()
app = Demo.app

def genPic2():
    while True:
        yield Demo.store.get_img2()

@app.route('/video_feed')
def video_feed():
    img = Demo.genPic()
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(img, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/things')
def things():
    img2 = genPic2()
    return Response(img2, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/state")
def get_state():
    label, state, isChange = Demo.store.get_status()
    return Response(json.dumps({"label": label, "state": state, "isChange": isChange}), mimetype='application/json')

@app.route('/')
def index():
    global Demo
    Demo.init_config()
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/<name>')
def show_person(name):
    passenger = Passengers.query.filter_by(name=name).first()
    prohibited = Prohibited_Items.query.filter_by(passenger_name = name).first()
    return render_template('user.html', passenger = passenger, prohibited = prohibited, base64=base64)

@app.route('/name')
def name():
    print(Demo.person)
    if Demo.person:
        return json.dumps({'name' : Demo.person.name})
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
