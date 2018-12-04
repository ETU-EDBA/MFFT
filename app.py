from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from jinja2 import Template
app = Flask(__name__, static_url_path='/static')
#Temporary db information
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://kitmfcqydctwdp:2ccac3a43a66c7a875f549659b949bf5fb2230902abb3581e87c70cb5108e5d5@ec2-54-75-231-3.eu-west-1.compute.amazonaws.com:5432/d4kvinmlpmn77t'
db = SQLAlchemy(app)


class Muzisyen(db.Model):
    __tablename__ = 'Muzisyen'

    MuzisyenId = db.Column('MuzisyenId', db.Integer, primary_key = True)
    MuzisyenAdi = db.Column(db.String(200))
    MuzisyenResmi = db.Column(db.String(200))
    MuzisyenKategorileri = db.relationship('MuzikKategorisi', backref='Muzisyen', lazy=True)
    MuzisyenSahneAlma= db.relationship('Festival', secondary='SahneAlma')

    def __init__(self, adi, resmi):
        self.MuzisyenAdi = adi
        self.MuzisyenResmi = resmi

class SahneAlma(db.Model):

    __tablename__='SahneAlma'
    SahneAlmaId = db.Column( db.Integer, primary_key = True)
    SahneAlmaMuzisyenId = db.Column('MuzisyenId', db.Integer, db.ForeignKey('Muzisyen.MuzisyenId'))
    SahneAlmaFestivalId = db.Column('FestivalId', db.Integer, db.ForeignKey('Festival.FestivalId'))
    def __init__(self, muzisyenid, festivalid):
        self.SahneAlmaMuzisyenId=muzisyenid
        self.SahneAlmaFestivalId=festivalid

class Festival(db.Model):
  __tablename__ = 'Festival'
  FestivalId = db.Column( db.Integer, primary_key = True)
  FestivalAdi = db.Column(db.String(100))
  FestivalAfisi = db.Column(db.String(400))
  FestivalAdresi = db.Column(db.String(200))
  FestivalBaslamaTarihi = db.Column(db.DateTime)
  FestivalAciklamasi = db.Column(db.String(400))
  FestivalBulunduguSehir = db.Column(db.String(50))
  FestivalSahneAlma=db.relationship('Muzisyen', secondary='SahneAlma')
  #FestivalIslemOzetleri = db.relationship('IslemOzeti', backref='Festival', lazy=True)
  FestivalBiletleri = db.relationship('Bilet')


  def __init__(self, adi, afisi, adresi, baslamaTarihi, aciklamasi, bulunduguSehir):
      self.FestivalAdi = adi
      self.FestivalAfisi = afisi
      self.FestivalAdresi = adresi
      self.FestivalBaslamaTarihi = baslamaTarihi
      self.FestivalAciklamasi = aciklamasi
      self.FestivalBulunduguSehir = bulunduguSehir

class Bilet(db.Model):
    __tablename__ = 'Bilet'

    BiletId = db.Column( db.Integer, primary_key = True)
    BiletAdi = db.Column(db.String(100))
    BiletFiyati = db.Column(db.Integer)
    BiletFestivalId = db.Column(db.Integer, db.ForeignKey('Festival.FestivalId'))
    KalanBiletSayisi = db.Column(db.Integer)
    BiletIslemOzetleri = db.relationship('IslemOzeti')


    def __init__(self, adi, fiyati, festival, kalanbilet):
      self.BiletAdi = adi
      self.BiletFiyati = fiyati
      self.FestivalId = festival
      self.KalanBiletSayisi = kalanbilet


class Kullanici(db.Model):
    __tablename__ = 'Kullanici'

    KullaniciId = db.Column('KullaniciId', db.Integer, primary_key = True)
    KullaniciEmail = db.Column(db.String(100))
    KullaniciSifre = db.Column(db.String(50))
    KullaniciAdi = db.Column(db.String(50))
    KullaniciAdresi = db.Column(db.String(200))
    KullaniciBakiyesi = db.Column(db.Integer)
    KullaniciTuru = db.Column(db.String(50))
    KullaniciIslemOzetleri = db.relationship('IslemOzeti')

    def __init__(self, email, sifre, adi, adresi, bakiyesi, turu):
      self.KullaniciEmail = email
      self.KullaniciSifre = sifre
      self.KullaniciAdi = adi
      self.KullaniciAdresi = adresi
      self.KullaniciBakiyesi = bakiyesi
      self.KullaniciTuru = turu

class IslemOzeti(db.Model):
    __tablename__ = 'IslemOzeti'

    IslemId = db.Column('IslemId', db.Integer, primary_key = True)
    IslemPNR = db.Column(db.String(20))
    IslemTarihi = db.Column(db.DateTime)
    IslemKullaniciId = db.Column(db.Integer, db.ForeignKey('Kullanici.KullaniciId'))
    IslemBiletId = db.Column(db.Integer, db.ForeignKey('Bilet.BiletId'))
    #IslemFestivalId = db.Column(db.Integer, db.ForeignKey('Festival.FestivalId'))


    def __init__(self, pnr, islemtarihi, biletid, kullaniciid, festivalid):
        self.IslemPNR = pnr
        self.IslemTarihi = islemtarihi
        self.BiletId = biletid
        self.KullaniciId = kullaniciid
        self.FestivalId = festivalid

class MuzikKategorisi(db.Model):
    __tablename__ = 'MuzikKategorisi'
    KategoriId= db.Column('KategoriId', db.Integer, primary_key = True)
    KategoriAdi = db.Column('KategoriAdi', db.String(50))
    MuzikMuzisyenId = db.Column(db.Integer, db.ForeignKey('Muzisyen.MuzisyenId'))

    def __init__(self, kategoriAdi, muzisyen):
      self.KategoriAdi = name
      self.MuzisyenId = muzisyen

@app.route('/')
def hello_world():

    db.create_all()        #veritabanlarini olusturur.
    #newUser=students("burak@gmail.com","12345","Burak","Ankara", 0, "Normal")   #Yeni kullanici objesi olusturur.
    #db.session.add(newUser) #Bu student objesini veritabanina ekler
    #db.session.commit()    #Veritabanina bu degisiklikleri commitler

    return render_template('MainPage.html')
@app.route('/festival/<id>')
def route_fest(id):
    return render_template('Festival.html')
