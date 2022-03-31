from flask import Flask
from flask_login import LoginManager
from flask_msearch import Search

from flask_sqlalchemy import SQLAlchemy

import datetime

UPLOAD_FOLDER= './upload'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/lida'
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager(app)
db = SQLAlchemy(app)
search = Search()
search.init_app(app)