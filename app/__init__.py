import http
from flask import Flask
from flask_login import LoginManager
from flask_msearch import Search
from flask_mail import *
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://agropecuariali:dedeu123@mysql.agropecuarialida.kinghost.net/agropecuariali'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SECRET_KEY'] = 'secret'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

login_manager = LoginManager(app)
db = SQLAlchemy(app)

search = Search()
search.init_app(app)

mail=Mail(app)
mail.init_app(app)

otp = random.randint(0000,9999)