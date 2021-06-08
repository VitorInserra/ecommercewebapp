from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import Item, Store, User, CartItem, UserInfo
from . import db
import os

stores = Blueprint('stores', __name__)

#creating items#
@stores.route('/newitem/<storeid>', methods=['GET', 'POST'])
@login_required
def newitem(storeid):
    y = storeid
    if request.method=='POST':
        name = request.form.get('itemname')
        price = request.form.get('itemprice')
        category = request.form.get('category')
        notes = request.form.get('notes')

        image = request.files['itemimage']
        
        #imagename = image.filename
        save_path = 'website\static\images'

        try:
            #completeName = os.path.join(save_path, imagename)
            image.save(os.path.join(save_path, image.filename))

            newitem = Item(name=name, price=price, imagename=image.filename, category=category, notes=notes, store_id=storeid)
            db.session.add(newitem)
            db.session.commit()

            return redirect("/store/" + storeid)
        except:
            flash('Something went wrong.', category='error')
            return redirect(url_for('views.home'))

    try:
        return render_template("general/newitem.html")
    except:
        flash('Something went wrong.', category='error')
        return redirect(url_for('views.home'))
###

#shopping cart#
@stores.route('/shoppingcart', methods=['GET', 'POST'])
@login_required
def shoppingcart():
    cartitems = CartItem.query.filter_by(user_id=current_user.id).all()
    info = UserInfo.query.filter_by(user_id=current_user.id).first()

    try:
        return render_template("general/shoppingcart.html", cart=cartitems, info=info)
    except:
        flash('Something went wrong.', category='error')
        return redirect(url_for('views.home'))
#remove
@stores.route('/shoppingcart/remove/<itemid>', methods=['GET','POST'])
@login_required
def removefromcart(itemid):
    try:
        delcart = CartItem.query.filter_by(item_id=itemid).first()
        db.session.delete(delcart)
        db.session.commit()

        return redirect(url_for('stores.shoppingcart'))
    except:
        flash('Something went wrong.', category='error')
        return redirect(url_for('stores.shoppingcart'))
###

#buy#
@stores.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method=='POST':
        if request.form.get('Buy!')=='buy':
            cart = []
            itemid = 0

            itemid = int(itemid)
            for cartitemid in range(0, 100):
                cartitem = CartItem.query.filter_by(id=cartitemid).first()
                if cartitem:
                    if cartitem.user_id == current_user.id:
                        itemid = cartitem.item_id
                        currentitem = Item.query.filter_by(id=itemid).first()
                        cart.append(currentitem)

            info = UserInfo.query.filter_by(user_id=current_user.id).first()
            if info:
                if len(cart) > 0:
                    print(current_user.email)
                    print(info.adress, info.creditcard)
                    print(cart)
                    
                    for i in range(len(cart)):
                        delcart = CartItem.query.filter_by(id=cart[i].id).first()
                        db.session.delete(delcart)
                        db.session.commit()

                    flash('Items on their way!', category='success')
                    return redirect(url_for('views.home'))
                
                    

                elif len(cart)==0:
                    flash('No items in cart', category='error')
            else:
                flash('No billing information, please add to profile', category='error')

    return render_template("general/checkout.html")
###