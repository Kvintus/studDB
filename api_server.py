from flask import Flask, request, jsonify, make_response, Response
from sqlalchemy.sql.functions import func
from helpers.sqlClasses import *
from datetime import date
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

@app.route('/api/students/getOne')
def getStudent():
    if request.method == 'GET':
        studID = request.args.get('id')
        statusResponse = -1
        returnStudent = {}
        
        try:
            student = Students.query.filter_by(studentID = studID).first()
            
            returnStudent = {'id': int(student.studentID),
                                    'name': student.studentName,
                                    'surname': student.studentSurname,
                                    'email': student.studentEmail,
                                    'phone': student.studentPhone,
                                    'parentIDs': []
                                    }
            for parent in student.parents:
                returnStudent['parentIDs'].append(parent.parentID)

            statusResponse = 1
        except:
            statusResponse = -1

        return jsonify(status=statusResponse, student=returnStudent)

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


            today = date.today()
        
        for Classe in orderedClasses:
            ourResponse = {'id': Classe.classID,
                                 'letter': Classe.classLetter,
                                 'start': Classe.classStart,
                                 'room': Classe.classRoom,
                                 'name': str(Classe.classStart) + Classe.classLetter
                                 }
            
            differenceInDays = today - date(Classe['start'], 9, 1)
            if differenceInDays < 1461:
                if differenceInDays < 365 and differenceInDays > 0:
                    ourResponse['altname'] = 'I.'
                elif differenceInDays < 730 and differenceInDays > 365:
                    ourResponse['altname'] = 'II.'
                elif differenceInDays < 1095 and differenceInDays > 730:
                    ourResponse['altname'] = 'III.'
                elif differenceInDays < 1461 and differenceInDays > 730:
                    ourResponse['altname'] = 'IV.'
                
                ourResponse['altname'] += Classe.classLetter

            mainResponse.append(ourResponse)
        return jsonify(status=statusResponse, classes=mainResponse)

@app.route('/api/classes/getOne')
def getClass():
    if request.method == 'GET':
        classID = request.args.get('id')
        statusResponse = -1
        returnClass = {}
        
        try:
            ourClass = Class.query.filter_by(classID = classID).first()
            
            returnClass = {'id': int(ourClass.classID),
                            'letter': ourClass.classLetter,
                            'room': ourClass.classRoom,
                            'start': ourClass.classStart,
                            'pupils': [],
                            'professors' : []
                                    }

            for professor in ourClass.profs:
                returnClass['professors'].append(professor.profID)
            
            for pupil in ourClass.pupils:
                returnClass['pupils'].append(pupil.studentID)

            statusResponse = 1
        except:
            statusResponse = -1

        return jsonify(status=statusResponse, student=returnClass)

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
            
@app.route('/api/parents/getOne')
def getParent():
    if request.method == 'GET':
        parentID = request.args.get('id')
        statusResponse = -1
        returnParent = {}
        
        try:
            parent = Parent.query.filter_by(parentID = parentID).first()
            
            returnParent = {'id': int(parent.parentID),
                                    'name': parent.parentName,
                                    'surname': parent.parentSurname,
                                    'email': parent.parentEmail,
                                    'phone': parent.parentPhone,
                                    'childIDs': []
                                    }
            
            for child in parent.children:
                returnParent['childIDs'].append(child.studentID)
    
            statusResponse = 1
        except:
            statusResponse = -1

        return jsonify(status=statusResponse, student=returnParent)

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

@app.route('/api/professors/getOne')
def getProfesor():
    if request.method == 'GET':
        profID = request.args.get('id')
        statusResponse = -1
        returnProfessor = {}
        
        try:
            professor = Professor.query.filter_by(profID = profID).first()
            
            returnProfessor = {'id': int(professor.profID),
                                    'name': professor.profName,
                                    'surname': professor.profSurname,
                                    'email': professor.profEmail,
                                    'phone': professor.profPhone,
                                    'title': professor.profTitle,
                                    'loc': professor.profLoc,
                                    'adress': professor.profAdress,
                                    'classIDs': []
                                    }

            for cl in professor.classes:
                returnProfessor['classIDs'].append(cl.classID)

            statusResponse = 1
        except:
            statusResponse = -1

        return jsonify(status=statusResponse, student=returnProfessor)

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

@app.route('/api/classes/update', methods = ['POST'])
def updateClass():
    """ Updates a class """    
    
    try:
        reJson = request.get_json()
        ourClass = Class.query.filter_by(classID=reJson['id']).first()

        if 'classLetter' in reJson:
            ourClass.classLetter = reJson['classLetter']
        if 'classRoom' in reJson:
            ourClass.classRoom = reJson['classRoom']
        if 'classStart' in reJson:
            ourClass.classStart = reJson['classStart']

        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

##                       Parent manipulation                            ##
@app.route('/api/parents/add', methods = ['POST'])
def addParent():
    """ Adds a parent to a database """    
    
    try:
        parent =  Parent()
        reJson = request.get_json()

        parent.parentEmail = reJson['email']
        parent.parentName = reJson['name']
        parent.parentPhone = reJson['phone']
        parent.parentSurname = reJson['surname']
        parent.parentAdress = reJson['adress']

        if 'childrenIDs' in reJson:
            for childrenID in reJson['childrenIDs']:
                child = Students.query.filter_by(studentID = childrenID)
                parent.children.append(child)

        db.session.add(parent)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/parents/remove', methods = ['POST'])
def removeParent():
    """ Removes a parent from a database """    
    
    try:
        reJson = request.get_json()
        parent = Parent.query.filter_by(parentID=reJson['id']).first()
        
        db.session.delete(parent)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/parents/update', methods = ['POST'])
def updateParent():
    """ Updates a parent in the database """    
    
    try:
        reJson = request.get_json()

        # Find the parent to update
        parent = Parent.query.filter_by(parentID=reJson['id']).first()

        # Update
        if 'email' in reJson:
            parent.parentEmail = reJson['email']
        if 'name' in reJson:
            parent.parentName = reJson['name']
        if 'phone' in reJson:
            parent.parentPhone = reJson['phone']
        if 'surname' in reJson:
            parent.parentSurname = reJson['surname']
        if 'adress' in reJson:
            parent.parentAdress = reJson['adress']


        # Updating children
        if 'childrenIDs' in reJson:
            staying = []
            # If the kids are not in the new --> they got deleted
            for child in parent.children:
                if not child.studentID in reJson['childrenIDs']:
                    parent.children.remove(child)
                staying.append(child.studentID)
            
            # If they are in the new list but not in the old --> they got added
            # Getting only the new ones
            reJson['childrenIDs'] = list(set(reJson['childrenIDs'])- set(staying))
            for childID in reJson['childrenIDs']:
                child = Students.query.filter_by(studentID = childID)
                parent.children.append(child)
    
        db.session.commit() 
        return jsonify(succcess=True)

    except:
        return jsonify(success=False)

##                       Professor manipulation                            ##
@app.route('/api/professors/add', methods = ['POST'])
def addProfessor():
    """ Adds a professor to a database """    
    
    try:
        professor =  Professor()
        reJson = request.get_json()

        professor.profEmail = reJson['email']
        professor.profTitle = reJson['title']
        professor.profName = reJson['name']
        professor.profLoc = reJson['loc']
        professor.profPhone = reJson['phone']
        professor.profSurname = reJson['surname']
        professor.profAdress = reJson['adress']

        if 'classID' in reJson:
            professor.classes.clear()
            professor.classes.append(Class.query.filter_by(classID=reJson['classID']))
        

        db.session.add(professor)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/professors/remove', methods = ['POST'])
def removeProfessor():
    """ Removes a professor from a database """    
    
    try:
        reJson = request.get_json()
        professor = Professor.query.filter_by(profID=reJson['id']).first()
        
        db.session.delete(professor)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False)

@app.route('/api/professors/update', methods = ['POST'])
def updateProfessor():
    """ Updates a professor in the database """    
    
    try:
        reJson = request.get_json()

        # Find the parent to update
        professor = Professor.query.filter_by(profID=reJson['id']).first()

        # Update
        if 'email' in reJson:
            professor.profEmail = reJson['email']
        if 'name' in reJson:
            professor.profName = reJson['name']
        if 'phone' in reJson:
            professor.profPhone = reJson['phone']
        if 'surname' in reJson:
            professor.profSurname = reJson['surname']
        if 'adress' in reJson:
            professor.profAdress = reJson['adress']
        if 'title' in reJson:
            professor.profTitle = reJson['title']


        if 'classID' in reJson:
            professor.classes.clear()
            professor.classes.append(Class.query.filter_by(classID=reJson['classID']))
        
        db.session.commit() 
        return jsonify(succcess=True)

    except:
        return jsonify(success=False)

@app.route('/')
def index():
    return "<h1> StudDB API </h1>"

