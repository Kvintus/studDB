from flask import Flask, request, jsonify, make_response, Response
from sqlalchemy.sql.functions import func
from helpers.sqlClasses import *
import json
from apis import api


app_secret = 'thisisasupersecretkey'

app = Flask(__name__)
app.config['SECRET_KEY'] = app_secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'
db.init_app(app)
api.init_app(app)

@app.route('/')
def index():
    return "<h1> StudDB API </h1>"

