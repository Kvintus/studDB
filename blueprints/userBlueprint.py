from flask import Blueprint, request, jsonify, make_response, session
from passlib.hash import pbkdf2_sha256 as sha256
import jwt
import datetime
import os, sys, inspect


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import cfg
from core.sqlClasses import User

userBlueprint = Blueprint('user', __name__)

# No route because the blueprint has url_prefix
@userBlueprint.route('', methods=['POST'])
def verifyUserLoginAndLogin():
    """ Verifies a user login """
    reJson = request.get_json() 
        
    # Check if we got all the fields
    if not 'username' in reJson:
        return jsonify(success=False, message='You haven\'t specified the username!')
    if not 'password' in reJson:
        return jsonify(success=False, message='You haven\'t specified the password!')

    # Get the user from the database
    ourUser = User.query.filter_by(username=reJson['username']).first()

    # Check if there is user with that username, if not return an error
    if ourUser == None:
        return jsonify(success=False, message='There no user with the username {} in the database!'.format(reJson['username']))

    if sha256.verify(reJson['password'], ourUser.userHash):
        # Create the user payload
        userBasePayload = {
            'id': ourUser.userID,
            'username': ourUser.username,
            'privilege': ourUser.userPrivilege,
            'exp': datetime.datetime.utcnow() + cfg.app_timedeltaExpiration  # The token will expire after a day
        }

        userBasePayload['api_key'] = jwt.encode(userBasePayload, cfg.app_secret).decode()
        # The user has logged in successfully
        session['user'] = userBasePayload
        return jsonify(success=True, user=userBasePayload)
    else:
        return jsonify(success=False, message='Wrong password!')

@userBlueprint.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify(success=True)

@userBlueprint.route('/logged', methods=['POST'])
def checkIfLoggedIn():
    """ Checks if any user is logged in and if he is it returns him. """

    if 'user' in session:
        return jsonify(isLoggedIn=True, user=session['user'])
    else:
        return jsonify(isLoggedIn=False)
