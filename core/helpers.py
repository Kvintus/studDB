from functools import wraps
from flask import request, jsonify
import jwt
import os, sys, inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from api_server import app_secret

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        try:
            tokenData = jwt.decode(token, app_secret)
        except:
            return jsonify(message="Missing token")

        return f(tokenData=tokenData, *args, **kwargs)
    return decorated
