from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from flask_login import LoginManager
from flask_msearch import Search
from flask_mail import *
from flask_sqlalchemy import SQLAlchemy
import random

from sqlalchemy import ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.secret_key = os.environ.get('APP_K')
app.config['SECRET_KEY'] = os.environ.get('S_K')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('TRACK_MODIFICATIONS')

login_manager = LoginManager(app)
db = SQLAlchemy(app)

search = Search()
search.init_app(app)

mail=Mail(app)
mail.init_app(app)

otp = random.randint(0000,9999)