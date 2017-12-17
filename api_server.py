from flask import Flask, request, jsonify, make_response, Response
from sqlalchemy.sql.functions import func
from helpers.sqlClasses import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'
db.init_app(app)


# Importing all the blueprints
from blueprints.classesBlueprint import classes_mod
from blueprints.parentsBlueprint import parents_mod
from blueprints.studentsBlueprint import students_mod
from blueprints.professorsBlueprint import professors_mod

# Registering the blueprints
app.register_blueprint(classes_mod, url_prefix='/api/classes')
app.register_blueprint(parents_mod, url_prefix='/api/parents')
app.register_blueprint(students_mod, url_prefix='/api/students')
app.register_blueprint(professors_mod, url_prefix='/api/professors')

@app.route('/')
def index():
    return "<h1> StudDB API </h1>"

