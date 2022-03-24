import os

from app import app, db
from flask import abort, current_app, render_template_string
from flask.json import JSONEncoder
from sql_alchemy import SQLAlchemy
from flask_babel import Babel
from flask_security import (
    Security,
    SQLAlchemyUserDataStore,
    auth_required,
    current_user,
    hash_password,
    permissions_accepted,
    permissions_required,
    roles_accepted
)
from flask_security.models import fsqla_v2 as fsqla

app.json_encoder = JSONEncoder

fsqla.FsModels.set_db_info(db, user_table_name="users", role_table_name="users")

class Role(db.Model, fsqla.FSUserMixin):
    __tablename__ = 'users'
    blogs = db.relationship("Blog", backref="users", lazy="dynamic")

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.Text)
    text = db.Column(db.UnicodeText)

#setup of flask-security
user_datastore = SQLAlchemyUserDataStore(db, User, Role)
app.security = Security(app, user_datastore)

# Babel setup
Babel(app)
