from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from jinja2 import Template
from datetime import datetime
app = Flask(__name__, static_url_path='/static')
#Temporary db information
##This is not the real db uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gqntjjrecxrcdo:29cb95ba43e52116977889413dfaa087694850ee8b5600581cb28c99b075c967@ec2-54-228-197-249.eu-west-1.compute.amazonaws.com:5432/d1j7smdboqmtjs'
db = SQLAlchemy(app)



SahneAlma = db.Table('SahneAlma',
    db.Column('SahneAlmaFestivalId',db.Integer, db.ForeignKey('Festival.FestivalId'), nullable=False,primary_key=True),
    db.Column('SahneAlmaMuzisyenId', db.Integer, db.ForeignKey('Muzisyen.MuzisyenId'), nullable=False,primary_key=True)
)
#class SahneAlma(db.Model):
#    __tablename__ = 'SahneAlma'
#    SahneAlmaFestivalId = db.Column(db.Integer, db.ForeignKey(Festival.FestivalId), nullable=False,primary_key=True, lazy=True)
#    SahneAlmaMuzisyenId = db.Column( db.Integer, db.ForeignKey(muzisyen.MuzisyenId), nullable=False,primary_key=True, lazy=True)
class Festival(db.Model):
  __tablename__ = 'Festival'
  FestivalId = db.Column( db.Integer, primary_key = True)
  FestivalAdi = db.Column(db.String(100))
  FestivalAfisi = db.Column(db.String(400))
  FestivalAdresi = db.Column(db.String(200))
  FestivalBaslamaTarihi = db.Column(db.DateTime)
  FestivalBitisTarihi = db.Column(db.DateTime)
  FestivalAciklamasi = db.Column(db.String(400))
  FestivalBulunduguSehir = db.Column(db.String(50))
  FestivalBiletleri = db.relationship('Bilet', backref='festival', lazy=True)
  FestivalSahneAlma = db.relationship('Muzisyen', secondary=SahneAlma, backref='festival',lazy=True)

class Muzisyen(db.Model):
    __tablename__ = 'Muzisyen'
    MuzisyenId = db.Column('MuzisyenId', db.Integer, primary_key = True)
    MuzisyenAdi = db.Column(db.String(200))
    MuzisyenResmi = db.Column(db.String(200))
    MuzisyenKategori = db.Column(db.String(200))

class Bilet(db.Model):
    __tablename__ = 'Bilet'
    BiletId = db.Column( db.Integer, primary_key = True)
    BiletAdi = db.Column(db.String(100))
    BiletFiyati = db.Column(db.Integer)
    BiletFestivalId = db.Column(db.Integer, db.ForeignKey('Festival.FestivalId'), nullable=False)
    KalanBiletSayisi = db.Column(db.Integer)
    BiletIslemOzetleri = db.relationship('IslemOzeti', backref='bilet', lazy=True)


class IslemOzeti(db.Model):
    __tablename__ = 'IslemOzeti'
    IslemId = db.Column('IslemId', db.Integer, primary_key = True)
    IslemPNR = db.Column(db.String(20),nullable=False)
    IslemTarihi = db.Column(db.DateTime)
    IslemBiletId = db.Column(db.Integer, db.ForeignKey('Bilet.BiletId'),nullable=False)
    IslemKullaniciId = db.Column(db.Integer, db.ForeignKey('Kullanici.KullaniciId'),nullable=False)

class Kullanici(db.Model):
    __tablename__ = 'Kullanici'
    KullaniciId = db.Column('KullaniciId', db.Integer, primary_key = True)
    KullaniciEmail = db.Column(db.String(100), nullable=False)
    KullaniciSifre = db.Column(db.String(50),nullable=False)
    KullaniciAdi = db.Column(db.String(50))
    KullaniciAdresi = db.Column(db.String(200))
    KullaniciBakiyesi = db.Column(db.Integer)
    KullaniciTuru = db.Column(db.String(50))
    KullaniciIslemOzetleri = db.relationship('IslemOzeti',backref='kullanici', lazy=True)

@app.route('/')
def hello_world():
    #muzisyen1 = Muzisyen(MuzisyenAdi = 'cohen', MuzisyenResmi = 'yk', MuzisyenKategori = 'slow')
    #kullanici1 = Kullanici(KullaniciEmail = 'asli', KullaniciSifre = 'qwe', KullaniciAdi = 'asli', KullaniciAdresi = 'abc', KullaniciBakiyesi = 3  , KullaniciTuru = 'yıkık')
    #festival1 = Festival(FestivalAdi = 'bilmem', FestivalAfisi = '/static/festival.jpg', FestivalAdresi = 'tobb', FestivalBaslamaTarihi = datetime.now()  , FestivalBitisTarihi = datetime.now(), FestivalAciklamasi = 'ashdgj', FestivalBulunduguSehir = 'asdhgj')
    #db.session.add(muzisyen1)
    #db.session.add(kullanici1)
    #db.session.add(festival1)
    #db.session.commit()

    #db.create_all() #veritabanlarini olusturur.

    return render_template('MainPage.html')


@app.route('/festivals')
def route_fest2():
    festivals = Festival.query.all()
            #.filter(Festival.FestivalId == id)
    return render_template('Festivals.html',festivals = festivals)

@app.route('/festival/<id>')
def route_fest(id):
    festivals = Festival.query\
            .filter(Festival.FestivalId == id)

    return render_template('Festival.html', festivals = festivals )
