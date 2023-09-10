from . import db
from flask_login import UserMixin


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_url = db.Column(db.String())
    short_url = db.Column(db.String(),  unique=True)
    clicks = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    urls = db.relationship('Url')
