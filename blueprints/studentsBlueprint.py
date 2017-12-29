# Normal imports 
from flask import Blueprint, request, jsonify
from datetime import date
import os,sys,inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from helpers.sqlClasses import *

students_mod = Blueprint('students', __name__)

def getClassAltName(start, letter):
    today = date.today()
    differenceInDays = (today - date(int(start), 9, 1)).days
    altname = '' 

    if differenceInDays < 1461:
        if differenceInDays < 365 and differenceInDays > 0:
            altname = 'I.'
        elif differenceInDays < 730 and differenceInDays > 365:
            altname = 'II.'
        elif differenceInDays < 1095 and differenceInDays > 730:
            altname = 'III.'
        elif differenceInDays < 1461 and differenceInDays > 730:
            altname = 'IV.'
        
        altname += letter
        return altname
    else:
        return None


@students_mod.route('/')
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

@students_mod.route('/getOne')
def getStudent():
    if request.method == 'GET':
        studID = request.args.get('id')
        statusResponse = -1
        returnStudent = {}
        
        try:
            student = Students.query.filter_by(studentID = studID).first()
            if student is None:
                return jsonify(status=-1, message='There is no such student in the database')
            
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

##                       Student manipulation                            ##

@students_mod.route('/add', methods = ['POST'])
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

@students_mod.route('/remove', methods = ['POST'])
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

@students_mod.route('/update', methods = ['POST'])
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
                raise
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
