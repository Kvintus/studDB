from flask import Flask, flash, redirect, render_template, request, session, url_for
from cs50 import SQL
from helpers.sqlClasses import *

app = Flask(__name__)


@app.route('/')
def index():
    s = Students.query().all()
    return render_template('main_template.html' , ala = s)

app.run(host='0.0.0.0', port='8080')