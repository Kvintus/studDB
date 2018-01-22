from flask import Flask, request, jsonify, make_response, Response, redirect, render_template
from sqlalchemy.sql.functions import func
from core.sqlClasses import *
import json
from datetime import timedelta
from apis import apiBlueprint as api
from blueprints.userBlueprint import userBlueprint
import cfg
from flask_cors import CORS

app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")
CORS(app=app, supports_credentials=True)
app.config['SECRET_KEY'] = cfg.app_secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'

# User gets kicked after 1 day
app.permanent_session_lifetime = timedelta(days=1)
db.init_app(app)

app.register_blueprint(userBlueprint, url_prefix='/user')
app.register_blueprint(api)

''' 
@app.route('/')
def index():
    return redirect('/api/')
 '''
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
