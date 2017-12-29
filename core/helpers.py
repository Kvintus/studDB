from functools import wraps
from flask import request, jsonify
import jwt
import os, sys, inspect
from datetime import date

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
import cfg

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # If the user didn't specify the token
        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers.get('X-API-KEY')
        elif 'token' in request.args:
            token = request.args.get('token')
        else:
            return jsonify(message="The authorization token is missing...")
            

        try:
            tokenData = jwt.decode(token, cfg.app_secret)
        except:
            return jsonify(message="Invalid token")

        return f(tokenData=tokenData, *args, **kwargs)
    return decorated

def getClassAltName(start, letter):
    today = date.today()
    differenceInDays = (today - date(int(start), 9, 1)).days
    altname = '' 

    if differenceInDays < 1461:
        if differenceInDays < 365 and differenceInDays > 0:
            altname = 'I.'
        elif differenceInDays < 730 and differenceInDays > 365:
            altname = 'II.'
        elif differenceInDays < 1095 and differenceInDays > 730:
            altname = 'III.'
        elif differenceInDays < 1461 and differenceInDays > 730:
            altname = 'IV.'
        
        altname += letter
        return altname
    else:
        return None
