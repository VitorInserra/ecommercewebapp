#create login/authorized pages
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_cors import CORS
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
CORS(auth)

#normal sign up#
@auth.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        useremail = User.query.filter_by(email=email).first()
        userusername = User.query.filter_by(username=username).first()
        
        if useremail:
            flash('Email already in use.', category='error')
        elif len(email) < 4:
            flash('Invalid email', category='error')
        elif len(username) < 3:
            flash('Invalid username, must be more than 1 character', category='error')
        elif userusername:
            flash('username already in use!')
        elif password1 != password2:
            flash('Your passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must have more than 7 characters', category='error')
        else:
            try:
                new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'), role='user') #look at other hashing algorithms
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                flash('Account created!', category='success')

                return redirect(url_for('views.home'))
            except:
                flash('Something went wrong.', category='error')
                return redirect(url_for('views.home'))
    try:
        return render_template("auth/signup.html", user=current_user)
    except:
        flash('Something went wrong.', category='error')
        return redirect(url_for('views.home'))
#normal log in#
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): #checks user.password and password to see if they are the same
                try: 
                    login_user(user, remember=True)
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('views.home'))
                except:
                    flash('Something went wrong.', category='error')
                    return redirect(url_for('auth.login'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    try:
        return render_template("auth/login.html")
    except:
        flash('Something went wrong.', category='error')
        return redirect(url_for('views.home'))

#admin sign up#
@auth.route('/adminsignup', methods=['GET', 'POST'])
def adminsignup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        adminpass = request.form.get('adminpass')

        useremail = User.query.filter_by(email=email).first()
        userusername = User.query.filter_by(username=username).first()
        
        if useremail:
            flash('Email already in use.', category='error')
        elif len(email) < 4:
            flash('Invalid email', category='error')
        elif len(username) < 3:
            flash('Invalid username, must be more than 1 character', category='error')
        elif userusername:
            flash('username already in use!')
        elif password1 != password2:
            flash('Your passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must have more than 7 characters', category='error')
        
        #TODO: create random adminpass generator
        elif adminpass != 'eldemasiado':
            flash('Wrong Admin Pass', category='error')

        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'), role='admin') #look at other hashing algorithms
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')

            return redirect(url_for('views.home'))
    return render_template("auth/adminsignup.html")
#admin log in#
@auth.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        adminpass = request.form.get('adminpass')

        user = User.query.filter_by(email=email).first()
        if user:
            if adminpass == 'eldemasiado':
                if check_password_hash(user.password, password): #checks user.password and password to see if they are the same
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("auth/adminlogin.html", user=current_user)
###


#log out#
@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('views.home'))

    return render_template("auth/logout.html")
###