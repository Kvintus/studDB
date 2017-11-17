from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify, make_response, Response
from sqlalchemy.sql.functions import func
from helpers.sqlClasses import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'
db.init_app(app)


@app.route('/api/students')
def apiStudents():
    if request.method == 'GET':
        orderByArg = request.args.get('orderBy')
        print(request.args)
        statusResponse = -1
        orderedStudents = []
        mainResponse = []

        if orderByArg == "id":
            orderedStudents = Students.query.order_by(Students.studentID).all()
            statusResponse = 1
        elif orderByArg == "name":
            orderedStudents = Students.query.order_by(Students.studentName).all()
            statusResponse = 1
        elif orderByArg == "surname":
            orderedStudents = Students.query.order_by(Students.studentSurname).all()
            statusResponse = 1

        for student in orderedStudents:
            mainResponse.append({'id': int(student.studentID),
                                 'name': student.studentName,
                                 'surname': student.studentSurname,
                                 'email': student.studentEmail,
                                 'phone': student.studentPhone
                                 })

        return jsonify(status=statusResponse, students=mainResponse)

@app.route('/api/classes')
def apiClasses():
    if request.method == 'GET':
        orderByArg = request.args.get('orderBy')
        statusResponse = -1
        orderedStudents = []
        mainResponse = []
        tableWithPupils = orderedClasses = db.session.query(Class, func.count(relClassStudent.c.studentID).label('total')).join(relClassStudent).group_by(Class)

        if orderByArg == "id":
            orderedClasses = tableWithPupils.order_by(Class.classID).all()
            statusResponse = 1
        elif orderByArg == "start":
            orderedClasses = tableWithPupils.order_by(Class.classStart).all()
            statusResponse = 1
        elif orderByArg == "pupils":
            #Generate the table with number of pupils 
            orderedClasses = tableWithPupils.order_by('total').all()
            statusResponse = 1
        
        for Classe in orderedClasses:
            mainResponse.append({'id': Classe.Class.classID,
                                 'letter': Classe.Class.classLetter,
                                 'start': Classe.Class.classStart,
                                 'room': Classe.Class.classRoom,
                                 'pupils': Classe.total
                                 })

        return jsonify(status=statusResponse, classes=mainResponse)



@app.route('/')
def index():
    s = Students.query.all()
    return render_template('listStudents.html', ala=s)


app.run(host='0.0.0.0', port=8080, debug=True)
