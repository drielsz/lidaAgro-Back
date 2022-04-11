from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from flask_login import LoginManager
from flask_msearch import Search
from flask_mail import *
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.secret_key = os.environ.get('APP_K')
app.config['SECRET_KEY'] = os.environ.get('S_K')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_USE_TLS']= os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USE_SSL']= os.environ.get('MAIL_USE_SSL')

login_manager = LoginManager(app)
db = SQLAlchemy(app)

search = Search()
search.init_app(app)

mail=Mail(app)
mail.init_app(app)

otp = random.randint(0000,9999)