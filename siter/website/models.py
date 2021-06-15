from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    role = db.Column(db.String(150))

    cart = db.relationship('CartItem', backref="user")
    userinfo = db.relationship('UserInfo', backref="user")
    store = db.relationship('Store', backref="user")


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))

    creditcard = db.Column(db.String(20))
    adress = db.Column(db.String(150))


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
   

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    name = db.Column(db.String(150))
    logoname = db.Column(db.String(200))
    item = db.relationship('Item', backref="store")

    type1 = db.Column(db.String(150))
    type2 = db.Column(db.String(150))
    type3 = db.Column(db.String(150))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    category = db.Column(db.String(200))
    price = db.Column(db.Integer)
    imagename = db.Column(db.String(200))
    notes = db.Column(db.String(1000))
    
    store_id = db.Column(db.Integer, ForeignKey('store.id'))