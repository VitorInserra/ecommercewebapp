from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import Item, Store, User, UserInfo, CartItem, Browsesesh
from . import db
import os

# from storesrec import timetopoints

views = Blueprint('views', __name__)

def sortstores(category, type1):
    stores = Store.query.filter_by(type2=category, type1=type1).all()

    return stores

def timetopoints():

    browsesesh = Browsesesh.query.filter_by(user_id=current_user.id).all()

    for i in range (len(browsesesh)):
        for j in range (0, i):
            if browsesesh[i].browsetime and browsesesh[j].browsetime and browsesesh[i].browsetime < browsesesh[j].browsetime:
                temp = browsesesh[i]
                browsesesh[i] = browsesesh[j]
                browsesesh[j] = temp

    type1cong = []
    for i in range (len(browsesesh)):
        if browsesesh[i].type1 not in type1cong:
            type1cong.append(browsesesh[i].type1)
    
    type2cong = []
    for i in range (len(browsesesh)):
        if browsesesh[i].type2 not in type2cong:
            type2cong.append(browsesesh[i].type2)

    class ListHolder(): 
        def __init__(self, type1, type2):
            self.type1 = type1 
            self.type2 = type2

    return ListHolder(type1cong, type2cong)
    


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    holder = timetopoints()
    type1ls = holder.type1
    type2ls = holder.type2
    print(type1ls, type2ls)

    line1 = sortstores(type2ls[0], type1ls[0]) 
    line2 = sortstores(type2ls[1], type1ls[1])
    line3 = sortstores(type2ls[2], type1ls[2])
    line4 = sortstores(type2ls[3], type1ls[3])
        
    try:
        return render_template("general/home.html", line1=line1, lines2=line2, lines3=line3, line4=line4)
    except:
        flash('Try refreshing your page!', category='error')


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
                try:
                    info = UserInfo(user_id=current_user.id, creditcard=creditcard, adress=adress)
                    db.session.add(info)
                    db.session.commit()
                    return redirect(url_for('views.profile'))
                except:
                    flash('Something went wrong.', category='error')
                    return redirect(url_for('views.profile'))
    try:
        return render_template("profile/profile.html", info=info)
    except:
        flash('Oops! Something went wrong.', category='error')
        return redirect(url_for('views.home'))

@views.route('/deleteaccount', methods=['GET', 'POST'])
@login_required
def deleteaccount():
    if request.method=='POST':
        user = User.query.filter_by(id=current_user.id).first()

        store = Store.query.filter_by(user_id=current_user.id).first()
        if store:
            items = Item.query.filter_by(store_id=store.id).all()

        userinfo = UserInfo.query.filter_by(user_id=current_user.id).all()
        cartitems = CartItem.query.filter_by(user_id=current_user.id).all()
        try:
            if userinfo:
                db.session.delete(userinfo)
            if store:
                if items:
                    for item in items:
                        db.session.delete(item)

                db.session.delete(store)
            if cartitems:
                for cartitem in cartitems:
                    db.session.delete(cartitems)
        
            db.session.delete(user)

            db.session.commit()
        except:
            flash('Something went wrong.', category='error')
            return redirect(url_for('views.profile'))

    try:
        return render_template('profile/deleteaccount.html')
    except:
        flash('Something went wrong.', category='error')
        return redirect(url_for('views.home'))


#My store#
@views.route('/mystore', methods=['GET', 'POST'])
@login_required
def mystore():
    if current_user.role != 'admin':
        store = Store.query.filter_by(user_id=current_user.id).first()
        
        try:
            return render_template("profile/mystore.html", store=store)
        except:
            flash('A problem occured.', category='error')
            return redirect(url_for('views.profile'))
    else:
        stores = Store.query.filter_by(user_id=current_user.id).all()

        return render_template("general/adminmystores.html", stores=stores)
        

@views.route('/newstore', methods=['GET', 'POST'])
@login_required
def newstore():
    if not current_user.store or current_user.role=='admin':
        if request.method=='POST':
            name = request.form.get('storename')
            type1 = request.form.get('type1')
            type2 = request.form.get('type2')
            type3 = request.form.get('type3')
        
            #get image
            image = request.files['logo']

            save_path = 'website/Static/images/'

            image.save(os.path.join(save_path, image.filename))

            newstore = Store(name=name, logoname=image.filename, user_id=current_user.id, type1=type1, type2=type2, type3=type3)
            db.session.add(newstore)
            db.session.commit()

            return redirect(url_for('views.home'))
            # except:
            #     flash('Something went wrong.', category='error')
            #     return redirect(url_for('views.profile'))
    
    elif current_user.store and current_user.role!='admin':
        return redirect(url_for('views.home'))

    return render_template("profile/newstore.html")


@views.route('/removestore/<storeid>', methods=['GET', 'POST'])
@login_required
def removestore(storeid):
    store = Store.query.filter_by(id=storeid).first()
    items = Item.query.filter_by(store_id=storeid).all()
    if items:
        for item in items:
            db.session.delete(item)
    db.session.delete(store)
    db.session.commit()

    return redirect(url_for('views.mystore'))