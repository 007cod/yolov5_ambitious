from flask import Flask, render_template, Response,jsonify
import matplotlib
import json
import base64
import datetime
import random
from tools.datatools import add_banned_item, add_passenger, update_person
from tools.data_init import db, Prohibited_Items, Passengers
from tools.demo_init import demo
matplotlib.use('Agg')

Demo = demo()
app = Demo.app
store = Demo.store

@app.route('/video_feed')
def video_feed():
    img = Demo.get_main()
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(img, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/things')
def things():
    img2 = store.get_arg('x_ray_img')
    return Response(img2, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/state")
def get_state():
    label, state, isChange = store.arg['label'], store.arg['state'], store.arg['isChange']
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
    if Demo.person:
        return json.dumps({'name' : Demo.person.name})
    else: 
        return json.dumps({'name' : '无'})
    
@app.route('/Xray/<name>')
def Xray(name):
    passenger = Passengers.query.filter_by(name=name).first()
    Xray_img = base64.b64encode(passenger.Xray_image).decode()
    return json.dumps({'Xray_img' : Xray_img})


@app.route('/danger_items/<name>')
def danger_items(name):
    items = Prohibited_Items.query.filter_by(passenger_name=name,location='重庆').all()
    name = []
    img = []
    for item in items:
        img.append(base64.b64encode(item.image).decode())
        name.append(item.category)
    return json.dumps({'img' : img, 'name': name})


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
    add_passenger('kunkun', '北京', '123456789', '123456789012345678', '上海', 'G1234', data_kunkun,None)
    add_passenger('lanqiu', '北京', '123456789', '123456789012345678', '上海', 'G1234', data_lanqiu,None)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        init_data()
        app.run(debug=False, host="0.0.0.0")
