from flask import Flask, render_template, request, Response, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from jinja2 import Template
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from flask_login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm
from sqlalchemy import asc

from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, IntegerField
from wtforms.validators import Email, DataRequired
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
import os
from os.path import join, dirname, realpath


import string
import random
app = Flask(__name__, static_url_path='/static')
#Temporary db information
##This is not the real db uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gqntjjrecxrcdo:29cb95ba43e52116977889413dfaa087694850ee8b5600581cb28c99b075c967@ec2-54-228-197-249.eu-west-1.compute.amazonaws.com:5432/d1j7smdboqmtjs'
app.config['SECRET_KEY']='secret_xxx';
db = SQLAlchemy(app)

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class SignupForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Sifre',validators=[DataRequired()])
    adi = StringField('Ad',validators=[DataRequired()])
    adresi = StringField('Adres',validators=[DataRequired()])
    turu = SelectField('Uyelik Tipi',choices=[('normal', 'Normal Kullanici'), ('festival', 'Festival Kullanici')],validators=[DataRequired()])
class SigninForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Sifre')

class MuzisyenEkle(FlaskForm):
    adi = StringField('Muzisyen Adi')
    resmi = FileField('Muzisyen Resmi',validators=[FileRequired()])
    kategorisi = StringField('Kategorisi')

class FestivalEkle(FlaskForm):
    adi = StringField('Festival Adi')
    afisi = FileField('Festival Afisi',validators=[FileRequired()])
    adresi = StringField('Festival Adresi')
    baslamatarihi = StringField('Festival Baslama Tarihi')
    bitistarihi = StringField('Festival Bitis Tarihi')
    aciklamasi = StringField('Festival Aciklamasi')
    bulundugusehir = StringField('Festivalin Bulundugu Sehir')

class BiletEkle(FlaskForm):
    adi = StringField('Bilet Adi')
    fiyati = IntegerField('Bilet Fiyati')
    biletsayisi = IntegerField('Bilet Sayisi')



# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


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

  def __init__(self, adi, afisi, adresi, baslama, bitis, aciklamasi, bulundugusehir):
      self.FestivalAdi = adi
      self.FestivalAfisi = afisi
      self.FestivalAdresi = adresi
      self.FestivalBaslamaTarihi = baslama
      self.FestivalBitisTarihi = bitis
      self.FestivalAciklamasi = aciklamasi
      self.FestivalBulunduguSehir = bulundugusehir



class Muzisyen(db.Model):
    __tablename__ = 'Muzisyen'
    MuzisyenId = db.Column('MuzisyenId', db.Integer, primary_key = True)
    MuzisyenAdi = db.Column(db.String(200))
    MuzisyenResmi = db.Column(db.String(200))
    MuzisyenKategori = db.Column(db.String(200))

    def __init__(self, adi, resmi, kategori):
        self.MuzisyenAdi = adi
        self.MuzisyenResmi = resmi
        self.MuzisyenKategori = kategori

class Bilet(db.Model):
    __tablename__ = 'Bilet'
    BiletId = db.Column( db.Integer, primary_key = True)
    BiletAdi = db.Column(db.String(100))
    BiletFiyati = db.Column(db.Integer)
    BiletFestivalId = db.Column(db.Integer, db.ForeignKey('Festival.FestivalId'), nullable=False)
    KalanBiletSayisi = db.Column(db.Integer)
    BiletIslemOzetleri = db.relationship('IslemOzeti', backref='bilet', lazy=True)
    def __init__(self, adi, fiyati, festivalid, kalanbilet):
        self.BiletAdi = adi
        self.BiletFiyati = fiyati
        self.BiletFestivalId = festivalid
        self.KalanBiletSayisi = kalanbilet

class IslemOzeti(db.Model):
    __tablename__ = 'IslemOzeti'
    IslemId = db.Column('IslemId', db.Integer, primary_key = True)
    IslemPNR = db.Column(db.String(20),nullable=False)
    IslemTarihi = db.Column(db.DateTime)
    IslemBiletId = db.Column(db.Integer, db.ForeignKey('Bilet.BiletId'),nullable=False)
    IslemKullaniciId = db.Column(db.Integer, db.ForeignKey('Kullanici.KullaniciId'),nullable=False)

class Kullanici(db.Model, UserMixin):
    __tablename__ = 'Kullanici'
    KullaniciId = db.Column('KullaniciId', db.Integer, primary_key = True)
    KullaniciEmail = db.Column(db.String(100), nullable=False)
    KullaniciSifre = db.Column(db.String(50),nullable=False)
    KullaniciAdi = db.Column(db.String(50))
    KullaniciAdresi = db.Column(db.String(200))
    KullaniciBakiyesi = db.Column(db.Integer)
    KullaniciTuru = db.Column(db.String(50))
    KullaniciIslemOzetleri = db.relationship('IslemOzeti',backref='kullanici', lazy=True)

    def __init__(self, email, sifre, adi, adresi, turu):
        self.KullaniciEmail = email
        self.KullaniciSifre = sifre
        self.KullaniciAdi = adi
        self.KullaniciAdresi = adresi
        self.KullaniciBakiyesi = 10000
        self.KullaniciTuru = turu

    def __repr__(self):
        return "%s" % self.KullaniciEmail

    def get_id(self):
           return (self.KullaniciEmail)

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False


@app.route('/')
def main_page():
    festivals = Festival.query.order_by(asc(Festival.FestivalBaslamaTarihi)).limit(3).all()
            #.filter(Festival.FestivalId == id)
    #festival = Festival.query\
    #        .filter(Festival.FestivalId == 1).first()
    #tarkan = muzisyenler = Muzisyen.query\
    #        .filter(Muzisyen.MuzisyenId == 1).first()
    #festival.FestivalSahneAlma.append(tarkan)
    #db.session.commit()
    return render_template('MainPage.html',festivals = festivals)
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
@login_required
def route_satinalma(id):
    bilet = Bilet.query\
        .filter(Bilet.BiletId == id).first()
    kullanici = Kullanici.query\
        .filter(Kullanici.KullaniciId==current_user.KullaniciId).first()
    festival = Festival.query\
        .filter(Festival.FestivalId == bilet.BiletFestivalId).first()
    return render_template('SatinAlma.html',bilet = bilet,kullanici=kullanici,festival=festival)

@app.route('/islemozeti/<id>')
def route_islemozeti(id):
    bilet = Bilet.query\
        .filter(Bilet.BiletId == id).first()
    kullanici = Kullanici.query\
        .filter(Kullanici.KullaniciId==current_user.KullaniciId).first()
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




@app.route('/islemozetigoruntule/<id>')
def route_ioGoruntule(id):
    islemozeti = IslemOzeti.query\
            .filter(IslemOzeti.IslemId == id).first()
    bilet = Bilet.query\
            .filter(Bilet.BiletId == islemozeti.IslemBiletId).first()
    kullanici = Kullanici.query\
            .filter(Kullanici.KullaniciId == islemozeti.IslemKullaniciId).first()
    festival = Festival.query\
            .filter(Festival.FestivalId == bilet.BiletFestivalId).first()
    return render_template('islemOzetiGoruntule.html',festival = festival,islemozeti=islemozeti,bilet=bilet,kullanici=kullanici)

@app.route('/profil')
@login_required
def route_pro1():
    kullanici = Kullanici.query\
            .filter(Kullanici.KullaniciId == current_user.KullaniciId).first()
    islemozetleri = IslemOzeti.query\
            .filter(IslemOzeti.IslemKullaniciId == current_user.KullaniciId)
    return render_template('Profil.html',kullanici = kullanici,islemozetleri=islemozetleri)

@app.route('/festival/<id>')
def route_fest(id):
    x = 0
    muzisyenler = []
    festivals = Festival.query\
            .filter(Festival.FestivalId == id)
    biletler = Bilet.query\
            .filter(Bilet.BiletFestivalId == id)
    sahneAlmalar = db.session.query(SahneAlma).join(Festival).join(Muzisyen).filter(Festival.FestivalId == id).all()
    for sahnealma in sahneAlmalar:
        muzisyenler.insert(x,Muzisyen.query\
            .filter(Muzisyen.MuzisyenId == sahnealma.SahneAlmaMuzisyenId).first())
        x = x + 1
    return render_template('Festival.html', festivals = festivals, biletler = biletler,muzisyenler=muzisyenler )

@app.route('/muzisyenler')
def route_muz1():
    muzisyenler = Muzisyen.query.all()
    return render_template('muzisyenler.html',muzisyenler = muzisyenler)


@app.route('/muzisyen/<id>')
def route_muz2(id):
    x = 0
    festivals = []
    muzisyenler = Muzisyen.query\
            .filter(Muzisyen.MuzisyenId == id)
    sahneAlmalar = db.session.query(SahneAlma).join(Festival).join(Muzisyen).filter(Muzisyen.MuzisyenId == id).all()
    for sahnealma in sahneAlmalar:
        festivals.insert(x,Festival.query\
            .filter(Festival.FestivalId == sahnealma.SahneAlmaFestivalId).first())
        x = x + 1
    return render_template('muzisyen.html',muzisyenler = muzisyenler,festivals = festivals)


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


@app.route('/giris', methods=['GET', 'POST'])
def login():
    formGiris = SigninForm(request.form)
    if request.method == 'GET':
        return render_template('Login.html', form=formGiris)
    elif request.method == 'POST':
            user = Kullanici.query.filter_by(KullaniciEmail=formGiris.email.data).first()
            if user:
                if user.KullaniciSifre == formGiris.password.data:
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('main_page'))
                else:
                    flash('Wrong password')
                    return redirect("/giris")
            else:
                flash('user doesnt exist')
                return redirect("/giris")

@app.route('/kayit', methods=['GET', 'POST'])
def signup():
    formSignup = SignupForm()
    if request.method == 'GET':
        return render_template('Signup.html', form = formSignup)
    elif request.method == 'POST':
            if Kullanici.query.filter_by(KullaniciEmail=formSignup.email.data).first():
                flash('Email address already exists')
                return redirect("/kayit")
            else:
                newuser = Kullanici(formSignup.email.data, formSignup.password.data, formSignup.adi.data, formSignup.adresi.data, formSignup.turu.data)
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)
                return redirect("/")

@app.route("/cikis")
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(email):
    return Kullanici.query.filter_by(KullaniciEmail = email).first()

@app.route('/muzisyenekle', methods=['GET', 'POST'])
def muzisyenekleroute():

    formMuzisyen = MuzisyenEkle(CombinedMultiDict((request.files, request.form)));
    if request.method == 'GET':
        return render_template('MuzisyenEkle.html', form = formMuzisyen)
    else:
        f = formMuzisyen.resmi.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            UPLOAD_FOLDER, filename
        ))
        yeniMuzisyen=Muzisyen(formMuzisyen.adi.data, filename, formMuzisyen.kategorisi.data)
        db.session.add(yeniMuzisyen)
        db.session.commit()
        flash('Muzisyen eklendi.')
        return redirect("/muzisyenekle")

@app.route('/festivalekle', methods=['GET', 'POST'])
def festivalekleroute():

    formFestival = FestivalEkle(CombinedMultiDict((request.files, request.form)));
    if request.method == 'GET':
        return render_template('FestivalEkle.html', form = formFestival)
    else:
        f = formFestival.afisi.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            UPLOAD_FOLDER, filename
        ))
        print(formFestival.baslamatarihi.data)
        yeniFestival=Festival(formFestival.adi.data, filename, formFestival.adresi.data, datetime.strptime(formFestival.baslamatarihi.data, '%Y-%m-%d'), datetime.strptime(formFestival.bitistarihi.data, '%Y-%m-%d'), formFestival.aciklamasi.data, formFestival.bulundugusehir.data)
        db.session.add(yeniFestival)
        db.session.commit()
        flash('Festival eklendi.')
        return redirect("/festivalekle")

def addSahneAlma(festivalId,muzisyenId):
    festival = Festival.query\
            .filter(Festival.FestivalId == festivalId).first()
    muzisyen = Muzisyen.query\
            .filter(Muzisyen.MuzisyenId == muzisyenId).first()
    festival.FestivalSahneAlma.append(muzisyen)
    db.session.commit()

@app.route('/festivalmuzisyenekle/<id>', methods=['GET', 'POST'])
def festivalmuzisyenekle(id):
    muzisyenlistesi=Muzisyen.query.all()
    if request.method == 'GET':
        return render_template('FestivalMuzisyenEkle.html', festivalid=id, muzisyenlistesi = muzisyenlistesi)

@app.route('/festivalmuzisyenekle/<id1>/<id2>', methods=['GET', 'POST'])
def festivalmuzisyenekle2(id1, id2):
    muzisyenlistesi=Muzisyen.query.all()
    if request.method == 'GET':
        addSahneAlma(id1,id2)
        flash('Festivale muzisyen eklendi.')
        return render_template('FestivalMuzisyenEkle.html', festivalid=id, muzisyenlistesi = muzisyenlistesi)


@app.route('/festivalbiletekle/<id>', methods=['GET', 'POST'])
def festivalbiletekleroute(id):

    formBilet = BiletEkle(request.form);
    if request.method == 'GET':
        return render_template('FestivalBiletEkle.html', form = formBilet, festivalid=id)
    else:
        yeniBilet=Bilet(formBilet.adi.data, formBilet.fiyati.data, id, formBilet.biletsayisi.data)
        db.session.add(yeniBilet)
        db.session.commit()
        flash('Festivale bilet eklendi.')
        return redirect("/festivalbiletekle/"+id)
