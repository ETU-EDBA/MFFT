from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from jinja2 import Template
app = Flask(__name__)
#Temporary db information
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gjsvisnidpytcu:1384bad225c73da42ffa760095e745251dc9815a1b482473e4100170f400e8fd@ec2-54-217-216-149.eu-west-1.compute.amazonaws.com:5432/d4tpgmffimbnjd'
db = SQLAlchemy(app)

#class students(db.Model):
#   id = db.Column('student_id', db.Integer, primary_key = True)
#   name = db.Column(db.String(100))
#   city = db.Column(db.String(50))
#   addr = db.Column(db.String(200))
#   pin = db.Column(db.String(10))

#   def __init__(self, name, city, addr,pin):
#       self.name = name
#       self.city = city
#       self.addr = addr
#       self.pin = pin

@app.route('/')
def hello_world():
    #db.create_all()        #veritabanlarini olusturur.
    #newStudent=students("ahmet","ankara","ank","06")   #Yeni student objesi olusturur.
    #db.session.add(newStudent) #Bu student objesini veritabanina ekler
    #db.session.commit()    #Veritabanina bu degisiklikleri commitler


    return render_template('index.html')
