from flask import Blueprint
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from .models import User, Browsesesh
from . import db

storesrec = Blueprint('storesrec', __name__)

def browsetime_derivative(userid, type2, type1):
#delta (currently 5)
    print("Running browsetime_derivative")
    browseseshs = Browsesesh.query.filter_by(user_id=userid, type2=type2, type1=type1).order_by(Browsesesh.id.desc()).all()
    print("Current seshs", browseseshs)

    roc = (browseseshs[0].browseend -  browseseshs[1].browseend)/2

    inf = [roc, type2, type1]
    print(inf)

    return inf


def list_stores():

    storetypes = [['mix', 'store'], ['clothes', 'store'], ['electronics', 'store'], ['furniture', 'store'], ['photography', 'store'], ['massage', 'store'], ['beauty', 'store'], ['music', 'store'], ['other', 'store']]
    der_values = []

    for i in range (0, len(storetypes)):
        try:
            der_values.append(browsetime_derivative(current_user.id, storetypes[i][0], storetypes[i][1]))
            print("This is der", der_values)
        except:
            print("No columns")

    #insertion sort:
    for i in range(1, len(der_values)):
        key = der_values[i]

        j = i-1
        while j >= 0 and key < der_values[j]:
            der_values[j+1] = der_values[j]
            j -= 1
        
        der_values[j+1] = key

    return der_values #sorted