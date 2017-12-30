import os, sys, inspect
from flask import Flask

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from core.sqlClasses import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../assets/database.db'
db.init_app(app)

with app.app_context():
    db.create_all()