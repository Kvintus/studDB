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

# Registering the blueprints
app.register_blueprint(classes_mod, url_prefix='/api/classes')
app.register_blueprint(parents_mod, url_prefix='/api/parents')


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
                                    'birth': student.studentDateOfBirth,
                                    'email': student.studentEmail,
                                    'start': student.studentStart,
                                    'class': {'id':'','name':''},
                                    'adress': student.studentAdress,
                                    'phone': student.studentPhone,
                                    'parents': []
                                    }
            
            for cl in student.classes:  
                returnStudent['class']['name'] = str(cl.classStart) + cl.classLetter
                returnStudent['class']['id'] = cl.classID
                altname = getClassAltName(cl.classStart, student.classes.first().classLetter)
                if altname != None:
                    returnStudent['class']['altname'] = altname 
            
            for parent in student.parents:
                ourParent = {'id': parent.parentID, 'wholeName': "{} {}".format(parent.parentName, parent.parentSurname)}
                returnStudent['parents'].append(ourParent)

            statusResponse = 1
        except:
            raise
            statusResponse = -1

        return jsonify(status=statusResponse, student=returnStudent)

 



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
                                    'surname': professor.profSurname,
                                    'title': professor.profTitle,
                                    'email': professor.profEmail,
                                    'phone':professor.profPhone
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
                                    'classes': []
                                    }


            for cl in professor.classes:
                ourClass = {} 
                ourClass['name'] = str(cl.classStart) + cl.classLetter
                ourClass['id'] = cl.classID
                altname = getClassAltName(cl.classStart, cl.classLetter)
                if altname != None:
                    ourClass['altname'] = altname 
                
                returnProfessor['classes'].append(ourClass)

            statusResponse = 1
        except:
            statusResponse = -1

        return jsonify(status=statusResponse, professor=returnProfessor)

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
        for parentID in reJson['parents']:
            try:
                parent = Parent.query.filter_by(parentID=parentID).first()
                student.parents.append(parent)
                print(student.parents[0].parentID) #Quick fix, without this it doesn't work !!!
            except:
                raise
                return jsonify(succcess=False, message="There is no parent with the ID {} in the database.".format(parentID))
        
        
        # Assigning the student a class
        if reJson['classID'] != None:
            try:
                newClass = Class.query.filter_by(classID=reJson['classID']).first()
                if newClass is not None:
                    student.classes.append(newClass)
                else:
                    return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['classID']))
            except:
                raise
                return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['classID']))

        db.session.add(student)
        db.session.commit()
        return jsonify(succcess=True, studentID=student.studentID)
    except:
        raise
        return jsonify(success=False)

@app.route('/api/students/remove', methods = ['POST'])
def removeStudent():
    """ Removes a student from a database """    
    
    try:
        reJson = request.get_json()
        student = Students.query.filter_by(studentID=reJson['id']).first()
        if student is not None:
            # Delete all relationships
            for parent in student.parents:
                student.parents.remove(parent)

            for cl in student.classes:
                student.classes.remove(cl)


            db.session.delete(student)
            db.session.commit()
            return jsonify(succcess=True)
        else:
            return jsonify(success=False, message="The user with ID {} doesn't exist.".format(reJson['id']))
    except:
        raise
        return jsonify(success=False)

@app.route('/api/students/update', methods = ['POST'])
def updateStudent():
    """ Updates a student in the database """    
    
    try:
        reJson = request.get_json()

        # Find the student to update
        try:
            student = Students.query.filter_by(studentID=int(reJson['id'])).first()
        except:
            raise
            return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(reJson['id']))
        
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
        for parent in student.parents:
            student.parents.remove(parent)

        for parentID in reJson['parents']:
            try:
                parent = Parent.query.filter_by(parentID=parentID).first()
                student.parents.append(parent)
                print(student.parents[0].parentID) #Quick fix, without this it doesn't work !!!
            except:
                return jsonify(succcess=False, message="There is no parent with the ID {} in the database.".format(parentID))
        
        
        
        # Assigning the student a class
        if 'classID' in reJson:
            if reJson['classID'] == 'remove':
                
                for classs in student.classes:
                    student.classes.remove(classs)

            else:
                try:
                    for classs in student.classes:
                        student.classes.remove(classs)

                    newClass = Class.query.filter_by(classID=reJson['classID']).first()
                    if newClass is not None:
                        student.classes.append(newClass)
                    else:
                        return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['classID']))
                except:
                    return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['classID']))
        
        db.session.commit() 
        return jsonify(success=True, studentName="{} {}".format(student.studentName, student.studentSurname))
    except:
        raise
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


        for classID in reJson['classes']:
            try:
                newClass = Class.query.filter_by(classID=classID).first()
                if newClass is not None:
                    professor.classes.append(newClass)
                else:
                    return jsonify(success=False, message="There is no class with the ID {} in the database.".format(classID))
            except:
                raise
                return jsonify(success=False, message="There is no class with the ID {} in the database.".format(classID))
        
        db.session.add(professor)
        db.session.commit()
        return jsonify(succcess=True, professorID=professor.profID)
    except:
        return jsonify(success=False)

@app.route('/api/professors/remove', methods = ['POST'])
def removeProfessor():
    """ Removes a professor from a database """    
    try:
        reJson = request.get_json()
        professor = Professor.query.filter_by(profID=reJson['id']).first()

        for cl in professor.classes:
                professor.classes.remove(cl)
        
        db.session.commit()
        db.session.delete(professor)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        raise
        return jsonify(success=False, message="There is no professor with the ID {} in the database.".format(reJson['id']))

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


        # Assigning the professor a class
        for classs in professor.classes:
                professor.classes.remove(classs)
        
        for classID in reJson['classes']:
            try:
                newClass = Class.query.filter_by(classID=classID).first()
                if newClass is not None:
                    professor.classes.append(newClass)
                else:
                    return jsonify(success=False, message="There is no class with the ID {} in the database.".format(classID))
            except:
                raise
                return jsonify(success=False, message="There is no class with the ID {} in the database.".format(classID))
        
        db.session.commit() 
        return jsonify(succcess=True, professorID=professor.profID)
    except:
        raise
        return jsonify(success=False, message='Fail')

@app.route('/')
def index():
    return "<h1> StudDB API </h1>"

