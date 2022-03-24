from flask import Flask
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/lida'
app.config['SECRET_KEY'] = 'secret'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


login_manager = LoginManager(app)
db = SQLAlchemy(app)
