# from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
# from flask_login import login_required, current_user
# from flask_sqlalchemy import SQLAlchemy
# from .models import Item, Store, User, UserInfo, CartItem, Browsesesh
# from . import db
# import os

# storesrec = Blueprint('storesrec', __name__)

# def timetopoints():

#     browsesesh = Browsesesh.query.filter_by(userid=current_user.id).all()

#     for i in range (len(browsesesh)):
#         for j in range (0, i):
#             if browsesesh[i] < browsesesh[j]:
#                 temp = browsesesh[i]
#                 browsesesh[i] = browsesesh[j]
#                 browsesesh[j] = temp
    
#     return browsesesh