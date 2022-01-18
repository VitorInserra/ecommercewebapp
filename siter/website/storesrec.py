from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import User, Browsesesh
from . import db
import os

storesrec = Blueprint('storesrec', __name__)

def browsetime_derivative(userid, storeid):
#delta (currently 5)
    browseseshH = Browsesesh.filter_by(user_id=userid, store_id=storeid).order_by(Browsesesh.id.desc()).first()
    browseseshA = Browsesesh.filter_by(user_id=userid, store_id=(storeid-5)).order_by(Browsesesh.id.desc()).first()

    roc = (browseseshH.browseend -  browseseshA.browseend)/5