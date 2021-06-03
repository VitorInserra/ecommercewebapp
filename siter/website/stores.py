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

        #completeName = os.path.join(save_path, imagename)
        image.save(os.path.join(save_path, image.filename))

        newitem = Item(name=name, price=price, imagename=image.filename, category=category, notes=notes, store_id=storeid)
        db.session.add(newitem)
        db.session.commit()

        return redirect("/store/" + storeid)

    return render_template("newitem.html")
###

#shopping cart#
@stores.route('/shoppingcart', methods=['GET', 'POST'])
@login_required
def shoppingcart():
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

    return render_template("shoppingcart.html", cart=cart, info=info)
#remove
@stores.route('/shoppingcart/remove/<itemid>', methods=['GET','POST'])
@login_required
def removefromcart(itemid):
    delcart = CartItem.query.filter_by(item_id=itemid).first()
    db.session.delete(delcart)
    db.session.commit()

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

                    flash('Itens estao a caminho', category='success')
                    return redirect(url_for('views.home'))
                
                    

                elif len(cart)==0:
                    flash('No items in cart', category='error')
            else:
                flash('No billing information, please add to profile', category='error')

    return render_template("checkout.html")
###


#Universal store route#
@stores.route('/store/<storeid>', methods=['GET', 'POST'])
@login_required
def callstore(storeid):
    store = Store.query.filter_by(id=storeid).first()

    items = []

    #change parameters as database grows#
    for itemid in range (0, 100):
        item = Item.query.filter_by(id=itemid).first()
        if item:
            if item.store_id == store.id:
                items.append(item)
                
    return render_template("estores/" + store.name + "/" + store.name + ".html", items=items, store=store)
#item page
@stores.route('/<storeid>/<id>', methods=['GET','POST'])
@login_required
def BFStoreitem(storeid, id): 
    item = Item.query.filter_by(id=id).first()
    store = Store.query.filter_by(id=storeid).first()

    #add to cart
    if request.method=='POST':    
        if request.form.get('addtocart') == 'addtocart':
            cartitem = CartItem(item_id=id, user_id=current_user.id)
            flash('Item successfully added', category='success')
            db.session.add(cartitem)
            db.session.commit()
    #   
    return render_template("estores/" + store.name + "/" + store.name + "item.html", item=item, store=store)
#removing items#
@stores.route('/removeitem/<storeid>/<itemid>')
@login_required
def removeitem(storeid, itemid):
    item = Item.query.filter_by(id=itemid).first()
    cartitem = CartItem.query.filter_by(item_id=itemid).first()
    if item:
        db.session.delete(item)
    if cartitem:
        db.session.delete(cartitem)
    
    db.session.commit()

    return redirect("/store/" + storeid)
###