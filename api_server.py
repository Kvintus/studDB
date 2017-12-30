from flask import Flask, request, jsonify, make_response, Response
from sqlalchemy.sql.functions import func
from core.sqlClasses import *
import json
from apis import apiBlueprint as api
import cfg


app = Flask(__name__)
app.config['SECRET_KEY'] = cfg.app_secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'
db.init_app(app)

app.register_blueprint(api)
