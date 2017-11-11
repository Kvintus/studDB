from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, Response, make_response
from helpers.sqlClasses import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'
db.init_app(app)

@app.route('/api')
def api():
    s = Students.query.order_by(Students.studentID).all()
    order = request.args.get('order')
    mainResponse = []

    for student in s:
        mainResponse.append({'name': student.studentName, 
        'surname': student.studentSurname, 
        'email': student.studentEmail, 
        'phone': student.studentPhone
        })
    
    return jsonify(result = mainResponse)

@app.route('/')
def index():
    s = Students.query.all()
    return render_template('listStudents.html', ala=s)


app.run(host='0.0.0.0', port=8080, debug=True)
