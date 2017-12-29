from functools import wraps
from flask import request, jsonify
import jwt
import os, sys, inspect

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
