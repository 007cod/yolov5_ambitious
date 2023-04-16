from tools.data_init import *
from flask_tools import app
import cv2
import pickle

def add_banned_item(category, location, time, passenger_name, passenger_id, image):
    banned_item = Prohibited_Items(category=category, location=location, time=time, passenger_name=passenger_name, passenger_id=passenger_id, image=image)
    db.session.add(banned_item)
    db.session.commit()

def add_passenger(name, address, phone, id_card_number, destination, train_number, photo, Xray_image):
    passenger = Passengers(name=name, address=address, phone=phone, id_card_number=id_card_number, destination=destination, train_number=train_number, photo=photo, Xray_image=Xray_image)
    db.session.add(passenger)
    db.session.commit()

def update_person(person, Xray_image):
    if Xray_image is None or person is None:
        return 
    Xray_image =  cv2.imencode('.png', Xray_image)[1].tobytes()
    name = person.name
    with app.app_context():
        passenger = Passengers.query.filter_by(name=name).one()
        passenger.Xray_image = Xray_image
        db.session.commit()

