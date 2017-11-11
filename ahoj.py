from flask import Flask, flash, redirect, render_template, request, session, url_for
from helpers.sqlClasses import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'
db.init_app(app)


@app.route('/')
def index():
    for student in Students.query.all():
        student.studentEmail = student.studentEmail.lower()
        db.session.commit()
    return 'Hi', 200


app.run(host='0.0.0.0', port=8080, debug=True)
