from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

class Prohibited_Items(db.Model):
    __tablename__ = 'prohibited_items'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    passenger_name = db.Column(db.String(50), nullable=False)
    passenger_id = db.Column(db.Integer,nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)

class Passengers(db.Model):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    id_card_number = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    train_number = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=True)
    Xray_image = db.Column(db.LargeBinary, nullable=True)