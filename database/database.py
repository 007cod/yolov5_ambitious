import sqlite3
from flask_sqlalchemy import SQLAlchemy
# 连接到数据库
conn = sqlite3.connect('C:\\Users\\DELL\Desktop\\项目\\yolov5_ambitious\\database\\person.db')
def create_table():
    conn.execute('''drop table Passengers;''')
    conn.execute('''drop table Prohibited_Items;''')
    conn.execute('''CREATE TABLE Passengers
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name string(50) NOT NULL,
                address string(50) NOT NULL,
                phone string(50) NOT NULL,
                id_card_number string(50) NOT NULL,
                destination string(50) NOT NULL,
                train_number string(50) NOT NULL,
                photo blob,
                Xray_image blob);''')

    # 创建prohibited_items表
    conn.execute('''CREATE TABLE Prohibited_Items
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                category string(50) NOT NULL,
                location string(50) NOT NULL,
                time string(50) NOT NULL,
                passenger_name string(50) NOT NULL,
                passenger_id INTEGER NOT NULL,
                image blob,
                FOREIGN KEY(passenger_id) REFERENCES Passengers(id));''')
    
def add_sample_data():
    # 添加样例passenger数据
    with open('./static/images/kunkun.jpg', 'rb') as f:
        image_data = f.read()
        conn.execute('''INSERT INTO Passengers (name, address, phone, id_card_number, destination, train_number, photo)
                VALUES ('kunkun', 'Beijing', '123456789', '123456789012345678', 'Shanghai', 'G1234', ?)''',(image_data,))
    with open('./static/images/avatar.jpeg', 'rb') as f:
        image_data = f.read()
        conn.execute('''INSERT INTO Passengers (name, address, phone, id_card_number, destination, train_number, photo)
                VALUES ('Bob', 'Shanghai', '987654321', '987654321098765432', 'Beijing', 'G5678', ?)''',(image_data,))
    # 添加样例prohibited_items数据
    # 假设Alice携带了违禁品
    passenger_id = conn.execute('''SELECT id FROM Passengers WHERE name=?''', ('kunkun',)).fetchone()[0]
    conn.execute('''INSERT INTO Prohibited_Items (category, location, time, passenger_name, passenger_id)
                VALUES ('knife', 'bag', '2023-04-20 10:00:00', 'kunkun', ?)''', (passenger_id,))

if __name__ == '__main__':
    create_table()
    add_sample_data()
    #add()
    # 提交更改
    conn.commit()

    # 关闭连接
    conn.close()
