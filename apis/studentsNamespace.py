# Normal imports
from flask import request, jsonify
from flask_restplus import Api, Namespace, fields, Resource, reqparse
from datetime import date
from .helpers import *
import os
import sys
import inspect

# Importing from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from core.sqlClasses import *
from core.helpers import token_required, getClassAltName

students_api = Namespace('students', 'Operations with students')

# Setting up ID only parser
idOnlyParser = reqparse.RequestParser()
idOnlyParser.add_argument('id', type=int, required=True, location="args")

idOnlyParserJson = students_api.model('DeleteEntry', {
    'id': fields.Integer(default=1, required=True)
})

# Setting up "First" parser
firstNArg = reqparse.RequestParser()
firstNArg.add_argument('first', type=int, required=False, location="args")

# Class schema to use a a nested element

classSchema = students_api.model = ('ClassSchema', {
    'id': fields.Integer(default=1, description="ID of the student's class"),
})

# Defining a newstudent model
newStudent = students_api.model('NewStudent', {
    'name': fields.String(default="John", required=True),
    'surname': fields.String(default="Doe", required=True),
    'birth': fields.String(default="1.1.2000", required=True),
    'email': fields.String(default="students@mail.com", required=True),
    'start': fields.Integer(default=date.today().year, required=True),
    'class': fields.Nested(classSchema),
    'adress': fields.String(default="Students Adress 16 NY", required=True),
    'phone': fields.String(default="+421 999 999 999", required=True),
    'parents': fields.List(fields.Integer(), description="IDs of the parrents")
})

# Defining an update model
updateStudent = students_api.model('UpdateStudent', {
    'id': fields.Integer(default=1, description='ID field of the student to update'),
    'name': fields.String(default="John", required=False),
    'surname': fields.String(default="Doe", required=False),
    'birth': fields.String(default="1.1.2000", required=False),
    'email': fields.String(default="students@mail.com", required=False),
    'start': fields.Integer(default=date.today().year, required=False),
    'class': fields.Nested(classSchema),
    'adress': fields.String(default="Students Adress 16 NY", required=False),
    'phone': fields.String(default="+421 999 999 999", required=False),
    'parents': fields.List(fields.Integer(), description="IDs of the parrents")
})

## Helper functions ##


@students_api.route('/all')
class AllStudents(Resource):
    @students_api.expect(firstNArg)
    def get(self):
        """ Displays all the students """
        orderByArg = request.args.get('orderBy')
        orderedStudents = []
        mainResponse = []
        firstN = None

        if 'first' in request.args:
            firstN = int(request.args['first'])

        if orderByArg == "id" or not orderByArg:
            orderedStudents = Students.query.order_by(Students.studentID).limit(firstN).all()
            statusResponse = 1
        elif orderByArg == "name":
            orderedStudents = Students.query.order_by(Students.studentName).limit(firstN).all()
            statusResponse = 1
        elif orderByArg == "surname":
            orderedStudents = Students.query.order_by(Students.studentSurname).limit(firstN).all()
            statusResponse = 1

        for student in orderedStudents:
            mainResponse.append({'id': int(student.studentID),
                                 'name': student.studentName,
                                 'surname': student.studentSurname,
                                 'email': student.studentEmail,
                                 'phone': student.studentPhone
                                 })

        return jsonify(success=True, students=mainResponse)


@students_api.route('')
class Student(Resource):
    """ Student namespace """

    @students_api.expect(idOnlyParser)
    def get(self):
        """ Gets one student """

        if not 'id' in request.args:
            return jsonify(success=False, message='No student is specified')

        studID = request.args.get('id')
        statusResponse = -1
        returnStudent = {}

        try:
            student = Students.query.filter_by(studentID=studID).first()
            if student is None:
                return jsonify(success=False, message='There is no such student in the database')

            returnStudent = {
                'id': int(student.studentID),
                'name': student.studentName,
                'surname': student.studentSurname,
                'birth': student.studentDateOfBirth,
                'email': student.studentEmail,
                'start': student.studentStart,
                'class': {'id': '', 'name': ''},
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
            statusResponse = -1

        return jsonify(success=True, student=returnStudent)

    @students_api.expect(newStudent)
    @students_api.doc(security='apikey')
    @token_required
    def post(self, tokenData):
        """ Adds a student to a database """
        if tokenData['privilege'] < 3:
            return jsonify(success=False, message="You dont't have privilege to add students")

        try:
            student = Students()
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
                    if parent == None:
                        return jsonify(success=False, message="There is no parent with the ID {} in the database.".format(parentID))

                    student.parents.append(parent)
                except:
                    return jsonify(success=False, message="There is no parent with the ID {} in the database.".format(parentID))

            # Assigning the student a class
            if reJson['class']['id'] != None:
                try:
                    newClass = Class.query.filter_by(classID=reJson['class']['id']).first()
                    if newClass is not None:
                        student.classes.append(newClass)
                    else:
                        return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['class']['id']))
                except:
                    return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['class']['id']))

            db.session.add(student)
            db.session.commit()
            return jsonify(success=True, studentID=student.studentID)
        except:
            return jsonify(success=False)

    @students_api.expect(idOnlyParserJson)
    @students_api.doc(security='apikey')
    @token_required
    def delete(self, tokenData):
        """ Removes a student from a database """

        if tokenData['privilege'] < 3:
            return jsonify(success=False, message="You don't have privilege to delete students")

        try:
            reJson = request.get_json()
            student = Students.query.filter_by(studentID=reJson['id']).first()
            if student is not None:
                # Delete all relationships
                deleteAllParents(student)
                deleteAllClasses(student)

                db.session.delete(student)
                db.session.commit()
                return jsonify(success=True)
            else:
                return jsonify(success=False, message="The user with ID {} doesn't exist.".format(reJson['id']))
        except:
            raise
            return jsonify(success=False)

    @students_api.doc(security='apikey')
    @students_api.expect(updateStudent)
    @token_required
    def put(self, tokenData):
        """ Edits a student in the database """

        if tokenData['privilege'] < 3:
            return jsonify(success=False, message="You don't have privilege to update students")

        try:
            reJson = request.get_json()

            # Find the student to update
            try:
                student = Students.query.filter_by(studentID=int(reJson['id'])).first()
            except:
                return jsonify(success=False, message="There is no student with the ID {} in the database.".format(reJson['id']))

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

            # Adding his parents but first removing the old ones
            deleteAllParents(student)

            for parentID in reJson['parents']:
                try:
                    parent = Parent.query.filter_by(parentID=parentID).first()

                    if parent == None:
                        return jsonify(success=False, message="There is no parent with the ID {} in the database.".format(parentID))

                    student.parents.append(parent)
                except:
                    return jsonify(success=False, message="There is no parent with the ID {} in the database.".format(parentID))

            # Assigning the student a class
            if 'class' in reJson and 'id' in reJson['class']:

                # First remove all the classes
                deleteAllClasses(student)

                if reJson['class']['id'] != '':
                    try:
                        for classs in student.classes:
                            student.classes.remove(classs)

                        newClass = Class.query.filter_by(classID=reJson['class']['id']).first()
                        if newClass is not None:
                            student.classes.append(newClass)
                        else:
                            return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['class']['id']))
                    except:
                        return jsonify(success=False, message="There is no class with the ID {} in the database.".format(reJson['class']['id']))

            db.session.commit()
            return jsonify(success=True, id=reJson['id'], studentName="{} {}".format(student.studentName, student.studentSurname))
        except:
            return jsonify(success=False)
