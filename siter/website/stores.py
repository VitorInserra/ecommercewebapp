from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from .models import Item, Store, User, CartItem, UserInfo, Browsesesh
from . import db


stores = Blueprint('stores', __name__)

#creating items#
@stores.route('/newitem/<storeid>', methods=['GET', 'POST'])
@login_required
def newitem(storeid):
    if current_user.store:
        if request.method=='POST':
            name = request.form.get('itemname')
            price = request.form.get('itemprice')
            category = request.form.get('category')
            notes = request.form.get('notes')

            #image = request.files['itemimage']
        
            #imagename = image.filename
            #save_path = 'website\static\images'

            try:
                #completeName = os.path.join(save_path, imagename)
                #image.save(os.path.join(save_path, image.filename))

                newitem = Item(name=name, price=price, category=category, notes=notes, store_id=storeid)
                db.session.add(newitem)
                db.session.commit()

                return redirect("/store/" + storeid)
            except:
                flash('Something went wrong.', category='error')
                return redirect(url_for('views.home'))

        return render_template("stores/newitem.html")

    else:
        return redirect(url_for('views.home'))
###

#shopping cart#
@stores.route('/shoppingcart', methods=['GET', 'POST'])
@login_required
def shoppingcart():
    cart = []
    cartitems = CartItem.query.filter_by(user_id=current_user.id).all()
    for i in cartitems:
        cart.append(Item.query.filter_by(id=i.item_id).first())
    info = UserInfo.query.filter_by(user_id=current_user.id).first()

    if request.method=='POST':
        if request.form.get('buy')=='Buy':
            for cartitem in cartitems:
                db.session.delete(cartitem)
            
            db.session.commit()

            flash('TO DO', category='Success')
            return redirect(url_for('views.home'))

    try:
        return render_template("stores/shoppingcart.html", cart=cart, info=info)
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

#Stores#
@stores.route('/store/<storeid>', methods=['GET','POST'])
@login_required
def store(storeid):

    store = Store.query.filter_by(id=storeid).first()
    items = Item.query.filter_by(store_id=storeid).all()

    return render_template('stores/store.html', items=items, store=store, user=current_user)
#item page

@stores.route('/item/<itemid>', methods=['GET', 'POST'])
@login_required
def item(itemid):
    item = Item.query.filter_by(id=itemid).first()
    store = Store.query.filter_by(id=item.store_id).first()

    if request.method=='POST':
        if request.form.get('Add to cart')=='add':
            if item:
                try:
                    cartitem = CartItem(item_id=item.id, user_id=current_user.id)
                    db.session.add(cartitem)
                    db.session.commit()

                    flash('Added to cart', category='success')
                    return redirect("/item/" + itemid)
            
                except:
                    flash('An error occured', category='error')
                    return redirect(url_for('views.home'))
            else:
                flash('An error occured', category='error')
                return redirect(url_for('views.home'))

    return render_template('stores/itempage.html', item=item, store=store, user=current_user)

#transition onunload -> from def store to ajaxrequest#
@stores.route(('/prerequest/<userid>/<storeid>'), methods=['GET', 'POST'])
def prerequest(userid, storeid):
    browsestart = request.args['browsestart']
    print(browsestart)
    
    store = Store.query.filter_by(id=storeid).first()

    browsesesh = Browsesesh(user_id=userid, store_id=store.id, type1=store.type1, type2=store.type2, browsestart=browsestart)
    db.session.add(browsesesh)
    db.session.commit()

    foo = 'complete'

    return foo


@stores.route(('/postrequest/<userid>/<storeid>'), methods=['GET', 'POST'])
def postrequest(userid, storeid):
    browsesesh = Browsesesh.query.filter_by(user_id=userid, store_id=storeid).order_by(Browsesesh.id.desc()).first()
    print(browsesesh.id)

    browsestart = browsesesh.browsestart


    browseend = request.args['browseend']
    browseend = int(browseend)
    print(browseend)

    browsesesh.browseend = browseend
    browsesesh.browsetime = browseend - browsestart
    print(browsesesh.browsetime)
    db.session.commit()

    foo = 'complete'

    return foo
    #pull browsestart from database then browsetime = browseend - browsestart