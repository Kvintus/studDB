from flask import Flask, request, jsonify, make_response, Response
from sqlalchemy.sql.functions import func
from helpers.sqlClasses import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets/database.db'
db.init_app(app)

# Providing info 
################
@app.route('/api/students')
def apiStudents():
    if request.method == 'GET':
        orderByArg = request.args.get('orderBy')
        statusResponse = -1
        orderedStudents = []
        mainResponse = []

        if orderByArg == "id" or not orderByArg:
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
        allClasses = Class.query.all()

        if orderByArg == "id" or not orderByArg:
            orderedClasses = Class.query.order_by(Class.classID).all()
            statusResponse = 1
        elif orderByArg == "start":
            orderedClasses = Class.query.order_by(Class.classStart).all()
            statusResponse = 1
        
        for Classe in orderedClasses:
            mainResponse.append({'id': Classe.classID,
                                 'letter': Classe.classLetter,
                                 'start': Classe.classStart,
                                 'room': Classe.classRoom,
                                 })

        return jsonify(status=statusResponse, classes=mainResponse)

@app.route('/api/parents')
def apiParents():
    if request.method == "GET":
        orderByArg = request.args.get('orderBy')
        statusResponse = -1
        orderedParents = []
        mainResponse = []

        if orderByArg == "id" or not orderByArg:
            orderedParents = Parent.query.order_by(Parent.parentID).all()
            statusResponse = 1
        elif orderByArg == "name":
            orderedParents = Parent.query.order_by(Parent.parentName).all()
            statusResponse = 1
        elif orderByArg == "surname":
            orderedParents = Parent.query.order_by(Parent.parentSurname).all()
            statusResponse = 1
        
        for parent in orderedParents:
            mainResponse.append({'id': parent.parentID,
                                    'name': parent.parentName,
                                    'surname': parent.parentSurname
                                    })
        
        return jsonify(status = statusResponse, parents = mainResponse)
            
 
@app.route('/api/professors')
def apiProfessors():
    if request.method == "GET":
        orderByArg = request.args.get('orderBy')
        statusResponse = -1
        orderedParents = []
        mainResponse = []

        if orderByArg == "id" or not orderByArg:
            orderedProfessors = Professor.query.order_by(Professor.profID).all()
            statusResponse = 1
        elif orderByArg == "name":
            orderedProfessors = Professor.query.order_by(Professor.profName).all()
            statusResponse = 1
        elif orderByArg == "surname":
            orderedProfessors = Professor.query.order_by(Professor.profSurname).all()
            statusResponse = 1
        
        for professor in orderedProfessors:
            profR = {'id': professor.profID,
                                    'name': professor.profName,
                                    'surname': professor.profSurname
                                    }
            if len(professor.classes.all()) > 0:
                profR['class'] = professor.classes.first().classID
            else:
                profR['class'] = -1
            
            mainResponse.append(profR)
        
    return jsonify(status = statusResponse, professors = mainResponse)

###########################################################################
# Manipulating
###########################################################################

##                       Student manipulation                            ##

@app.route('/api/students/add', methods = ['POST'])
def addStudent():
    """ Adds a student to a database """    
    
    try:
        student =  Students()
        reJson = request.get_json()
        student.studentEmail = reJson['email']
        student.studentName = reJson['name']
        student.studentPhone = reJson['phone']
        student.studentSurname = reJson['surname']
        student.studentStart = reJson['start']
        student.studentAdress = reJson['adress']
        student.studentDateOfBirth = reJson['birth']

        # Adding his parents
        mother = Parent.query.filter_by(parentID=reJson['motherID']).first()
        father = Parent.query.filter_by(parentID=reJson['fatherID']).first()
        
        student.parents.append(mother)
        student.parents.append(father)


        # Assigning the student a class
        studentClass = Class.query.filter_by(classID=reJson['classID']).first()
        student.classes.append(studentClass)


        db.session.add(student)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/students/remove', methods = ['POST'])
def removeStudent():
    """ Removes a student from a database """    
    
    try:
        reJson = request.get_json()
        student = Students.query.filter_by(studentID=reJson['id']).first()
        db.session.delete(student)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/students/update', methods = ['POST'])
def updateStudent():
    """ Updates a student in the database """    
    
    try:
        reJson = request.get_json()

        # Find the student to update
        student = Students.query.filter_by(studentID=reJson['id']).first()

        # Update
        if 'email' in reJson:
            student.studentEmail = reJson['email']
        if 'name' in reJson:
            student.studentName = reJson['name']
        if 'phone' in reJson:
            student.studentPhone = reJson['phone']
        if 'surname' in reJson:
            student.studentSurname = reJson['surname']
        if 'start' in reJson:
            student.studentStart = reJson['start']
        if 'adress' in reJson:
            student.studentAdress = reJson['adress']
        if 'birth' in reJson:
            student.studentDateOfBirth = reJson['birth']

        # Adding his parents
        if 'motherID' in reJson:
            mother = Parent.query.filter_by(parentID=reJson['motherID']).first()
            student.parents[0] = mother
        if 'fatherID' in reJson:
            father = Parent.query.filter_by(parentID=reJson['fatherID']).first()
            student.parents[1] = father
        
        


        # Assigning the student a class
        if 'classID' in reJson:
            newClass = Class.query.filter_by(classID=reJson['classID']).first()
            student.classes[0] = newClass
    
        db.session.commit() 
        return jsonify(succcess=True)

    except:
        return jsonify(success=False)


##                       Class manipulation                            ##
@app.route('/api/classes/add', methods = ['POST'])
def addClass():
    """ Adds a class to a database """    
    
    try:
        reJson = request.get_json()

        newClass =  Class()
        newClass.classLetter = reJson['classLetter']
        newClass.classRoom = reJson['classRoom']
        newClass.classStart = reJson['classStart']

        db.session.add(newClass)
        print('adding new class')
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/classes/remove', methods = ['POST'])
def removeClass():
    """ Removes a class from a database """    
     
    try:
        reJson = request.get_json()
        ourClass = Class.query.filter_by(classID=reJson['classID']).first()

        db.session.delete(ourClass)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/classes/add', methods = ['POST'])
def updateClass():
    """ Updates a class """    
    
    try:
        reJson = request.get_json()
        ourClass = Class.query.filter_by(classID=reJson['id'])

        ourClass.classLetter = reJson['classLetter']
        ourClass.classRoom = reJson['classRoom']
        ourClass.classStart = reJson['classStart']

        db.session.add(newClass)
        print('adding new class')
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/')
def index():
    return "<h1> StudDB API </h1>"

