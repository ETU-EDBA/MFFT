from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from jinja2 import Template
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
import string
import random
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
    #db.create_all() #veritabanlarini olusturur.
    #muzisyen1 = Muzisyen(MuzisyenAdi = 'cohen', MuzisyenResmi = 'yk', MuzisyenKategori = 'slow')
    #kullanici1 = Kullanici(KullaniciEmail = 'asli', KullaniciSifre = 'qwe', KullaniciAdi = 'asli', KullaniciAdresi = 'abc', KullaniciBakiyesi = 3  , KullaniciTuru = 'yikik')
    #festival1 = Festival(FestivalAdi = 'JAZZ festival', FestivalAfisi = 'fest1.jpg', FestivalAdresi = 'istanbul', FestivalBaslamaTarihi = datetime.now()  , FestivalBitisTarihi = datetime.now(), FestivalAciklamasi = 'ol', FestivalBulunduguSehir = 'ist')
    #db.session.add(muzisyen1)
    #db.session.add(kullanici1)
    #db.session.add(festival1)
    #muzisyen1 = Muzisyen(MuzisyenAdi = 'Tarkan', MuzisyenResmi = 'Tarkan.jpg', MuzisyenKategori = 'Pop')
    #bilet1=Bilet(BiletAdi='VIP', BiletFiyati=1000,BiletFestivalId=1,KalanBiletSayisi=100)
    #db.session.add(bilet1)
    #db.session.commit()



    return render_template('MainPage.html')

@app.route('/satinal/<id>')
def route_satinalma(id):
    bilet = Bilet.query\
        .filter(Bilet.BiletId == id).first()
    kullanici = Kullanici.query\
        .filter(Kullanici.KullaniciId==1).first()
    festival = Festival.query\
        .filter(Festival.FestivalId == bilet.BiletFestivalId).first()
    return render_template('SatinAlma.html',bilet = bilet,kullanici=kullanici,festival=festival)

@app.route('/islemozeti/<id>')
def route_islemozeti(id):
    bilet = Bilet.query\
        .filter(Bilet.BiletId == id).first()
    kullanici = Kullanici.query\
        .filter(Kullanici.KullaniciId==1).first()
    festival = Festival.query\
        .filter(Festival.FestivalId == bilet.BiletFestivalId).first()
    kalanBakiye = kullanici.KullaniciBakiyesi - bilet.BiletFiyati
    if kalanBakiye < 0 or bilet.KalanBiletSayisi < 1:
        return render_template('bulamadik.html')
    else:
         bilet.KalanBiletSayisi = bilet.KalanBiletSayisi - 1
         kullanici.KullaniciBakiyesi = kalanBakiye
         pnr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
         islemozeti = IslemOzeti(IslemPNR=pnr,IslemTarihi= datetime.now(),IslemBiletId=bilet.BiletId,IslemKullaniciId=kullanici.KullaniciId)
         db.session.add(islemozeti)
         db.session.commit()
         return render_template('IslemOzeti.html',bilet = bilet, kullanici = kullanici, festival = festival, islemozeti=islemozeti)

@app.route('/festivals/<input>')
def route_fest3(input):
    festivals = Festival.query\
            .filter(Festival.FestivalAdi == input)
    xxx = Festival.query\
            .filter(Festival.FestivalAdi == input).count()
    if xxx == 0:
        return render_template('bulamadik.html')
    else:
        return render_template('Festivals.html',festivals = festivals)


@app.route('/festivals')
def route_fest2():
    festivals = Festival.query.all()
            #.filter(Festival.FestivalId == id)
    return render_template('Festivals.html',festivals = festivals)

@app.route('/festival/<id>')
def route_fest(id):
    festivals = Festival.query\
            .filter(Festival.FestivalId == id)
    biletler = Bilet.query\
            .filter(Bilet.BiletFestivalId == id)
    return render_template('Festival.html', festivals = festivals, biletler = biletler )

@app.route('/muzisyenler')
def route_muz1():
    muzisyenler = Muzisyen.query.all()
    return render_template('muzisyenler.html',muzisyenler = muzisyenler)


@app.route('/muzisyen/<id>')
def route_muz2(id):
    muzisyenler = Muzisyen.query\
            .filter(Muzisyen.MuzisyenId == id)
    return render_template('muzisyen.html',muzisyenler = muzisyenler)


@app.route('/muzisyenler/<input>')
def route_muz3(input):
    muzisyenler = Muzisyen.query\
            .filter(Muzisyen.MuzisyenAdi == input)
    xxx = Muzisyen.query\
            .filter(Muzisyen.MuzisyenAdi == input).count()
    if xxx == 0:
        return render_template('bulamadik.html')
    else:
        return render_template('muzisyenler.html',muzisyenler = muzisyenler)
