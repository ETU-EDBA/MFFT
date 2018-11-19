from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from jinja2 import Template
app = Flask(__name__)
#Temporary db information
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gjsvisnidpytcu:1384bad225c73da42ffa760095e745251dc9815a1b482473e4100170f400e8fd@ec2-54-217-216-149.eu-west-1.compute.amazonaws.com:5432/d4tpgmffimbnjd'
db = SQLAlchemy(app)


class Muzisyen(db.Model):
    __tablename__ = 'Muzisyen'

    MuzisyenId = db.Column('MuzisyenId', db.Integer, primary_key = True)
    MuzisyenAdi = db.Column(db.String(200))
    MuzisyenResmi = db.Column(db.String(200))
    MuzisyenKategorileri = db.relationship('MuzikKategorisi', backref='Muzisyen', lazy=True)


    def __init__(self, adi, resmi):
        self.MuzisyenAdi = adi
        self.MuzisyenResmi = resmi


SahneAlma = db.Table('SahneAlma',
    db.Column('MuzisyenId', db.Integer, db.ForeignKey('Muzisyen.MuzisyenId'), primary_key=True),
    db.Column('FestivalId', db.Integer, db.ForeignKey('Festival.FestivalId'), primary_key=True)
)
class Festival(db.Model):
  __tablename__ = 'Festival'


  FestivalId = db.Column( db.Integer, primary_key = True)
  FestivalAdi = db.Column(db.String(100))
  FestivalAfisi = db.Column(db.String(400))
  FestivalAdresi = db.Column(db.String(200))
  FestivalBaslamaTarihi = db.Column(db.DateTime)
  FestivalAciklamasi = db.Column(db.String(400))
  FestivalBulunduguSehir = db.Column(db.String(50))
  FestivalSahneler=db.relationship('Muzisyen', secondary=SahneAlma, lazy='subquery', backref=db.backref('Festival', lazy=True))
  FestivalIslemOzetleri = db.relationship('IslemOzeti', backref='Festival', lazy=True)
  FestivalBiletleri = db.relationship('Bilet', backref='Festival', lazy=True)


  def __init__(self, adi, afisi, adresi, baslamaTarihi, aciklamasi, bulunduguSehir):
      self.FestivalAdi = adi
      self.FestivalAfisi = afisi
      self.FestivalAdresi = adresi
      self.FestivalBaslamaTarihi = baslamaTarihi
      self.FestivalAciklamasi = aciklamasi
      self.FestivalBulunduguSehir = bulunduguSehir

class Bilet(db.Model):
    __tablename__ = 'Bilet'

    BiletId = db.Column('BiletId', db.Integer, primary_key = True)
    BiletAdi = db.Column(db.String(100))
    BiletFiyati = db.Column(db.Integer)
    BiletFestivalId = db.Column(db.Integer, db.ForeignKey('Festival.FestivalId'),
        nullable=False, primary_key=True)
    KalanBiletSayisi = db.Column(db.Integer)
    BiletIslemOzetleri = db.relationship('IslemOzeti', backref='Bilet', lazy=True)


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
    KullaniciIslemOzetleri = db.relationship('IslemOzeti', backref='Kullanici', lazy=True)

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
    IslemBiletId = db.Column(db.Integer, db.ForeignKey('Bilet.BiletId'),
        nullable=False)
    IslemKullaniciId = db.Column(db.Integer, db.ForeignKey('Kullanici.KullaniciId'),
        nullable=False)
    IslemFestivalId = db.Column(db.Integer, db.ForeignKey('Festival.FestivalId'),
        nullable=False)


    def __init__(self, pnr, islemtarihi, biletid, kullaniciid, festivalid):
        self.IslemPNR = pnr
        self.IslemTarihi = islemtarihi
        self.BiletId = biletid
        self.KullaniciId = kullaniciid
        self.FestivalId = festivalid

class MuzikKategorisi(db.Model):
    __tablename__ = 'MuzikKategorisi'

    KategoriAdi = db.Column('KategoriAdi', db.String(50), primary_key = True)
    MuzikMuzisyenId = db.Column(db.Integer, db.ForeignKey('Muzisyen.MuzisyenId'),
        nullable=False, primary_key=True)

    def __init__(self, kategoriAdi, muzisyen):
      self.KategoriAdi = name
      self.MuzisyenId = muzisyen

@app.route('/')
def hello_world():

    db.create_all()        #veritabanlarini olusturur.
    #newUser=students("burak@gmail.com","12345","Burak","Ankara", 0, "Normal")   #Yeni kullanici objesi olusturur.
    #db.session.add(newUser) #Bu student objesini veritabanina ekler
    #db.session.commit()    #Veritabanina bu degisiklikleri commitler


    return render_template('index.html')
