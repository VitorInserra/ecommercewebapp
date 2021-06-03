from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import Item, Store, User, UserInfo
from . import db
import os

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    storesls = []
    
    for storeid in range (0, 100): #change parameters as database grows
        currentstore = Store.query.filter_by(id=storeid).first()
        if currentstore:
                storesls.append(currentstore)

    return render_template("home.html", storesls=storesls, length=len(storesls), i=0)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    info = UserInfo.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        if request.form.get('send') == 'send':
            adress = request.form.get('adress')
            creditcard = request.form.get('creditcard')
      
            if len(creditcard) != 16:
                flash('Cartao invalido', category='error')
            
            else:
                info = UserInfo(user_id=current_user.id, creditcard=creditcard, adress=adress)
                db.session.add(info)
                db.session.commit()
                return redirect(url_for('views.profile'))

    return render_template("profile.html", info=info)

@views.route('/newstore', methods=['GET', 'POST'])
@login_required
def newstore():
    if request.method=='POST':
        name = request.form.get('storename')
        type1 = request.form.get('type1')
        type2 = request.form.get('type2')
        type3 = request.form.get('type3')
        
        #get image
        image = request.files['logo']

        save_path = 'website\static\images'

        image.save(os.path.join(save_path, image.filename))

        newstore = Store(name=name, logoname=image.filename, type1=type1, type2=type2, type3=type3)
        db.session.add(newstore)
        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template("newstore.html")

@views.route('/removestore/<storeid>')
@login_required
def removestore(storeid):
    store = Store.query.filter_by(id=storeid).first()
    db.session.delete(store)
    db.session.commit()

    return redirect(url_for('views.home'))