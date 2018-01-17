# Normal imports
from flask import request, jsonify
from flask_restplus import Api, Namespace, fields, Resource, reqparse
from datetime import date
from .helpers import deleteAllPupils, deleteAllProfessors
import os
import sys
import inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from core.sqlClasses import *
from core.helpers import *

# Creating blueprint
classes_api = Namespace('classes', 'Operations with classes')

# Setting up ID only parser
idOnlyParser = reqparse.RequestParser()
idOnlyParser.add_argument('id', type=int, required=True, location="args")

idOnlyParserJson = classes_api.model('DeleteEntry', {
    'id': fields.Integer(default=1, required=True)
})

# Setting up "First" parser
firstNArg = reqparse.RequestParser()
firstNArg.add_argument('first', type=int, required=False, location="args")

newClass = classes_api.model('NewClass',
                             {
                                 'letter': fields.String(default='A', required=True),
                                 'room': fields.String(default='P1', required=False),
                                 'start': fields.Integer(default=2017, required=True)
                             }
                             )

updateClass = classes_api.model('UpdateClass',
                                {
                                    'id': fields.Integer(default=1, required=True),
                                    'letter': fields.String(default='A', required=False),
                                    'room': fields.String(default='P1', required=False),
                                    'start': fields.Integer(default=2017, required=False)
                                }
                                )


@classes_api.route('/all')
class AllClasses(Resource):
    @classes_api.expect(firstNArg)
    def get(self):
        """ Returns all classes in the database """

        if request.method == 'GET':
            orderByArg = request.args.get('orderBy')
            orderedStudents = []
            mainResponse = []
            firstN = None

            if 'first' in request.args:
                firstN = int(request.args['first'])

            if orderByArg == "id" or not orderByArg:
                orderedClasses = Class.query.order_by(Class.classID).limit(firstN).all()
            elif orderByArg == "start":
                orderedClasses = Class.query.order_by(Class.classStart).limit(firstN).all()

            for Classe in orderedClasses:
                ourResponse = {'id': Classe.classID,
                               'letter': Classe.classLetter,
                               'start': Classe.classStart,
                               'room': Classe.classRoom,
                               'name': str(Classe.classStart) + Classe.classLetter
                               }

                altname = getClassAltName(Classe.classStart, Classe.classLetter)
                if altname != None:
                    ourResponse['altname'] = altname

                mainResponse.append(ourResponse)
            return jsonify(success=True, classes=mainResponse)


@classes_api.route('')
class OneClass(Resource):

    @classes_api.expect(idOnlyParser)
    def get(self):
        """ Returns a specific class """
        classID = request.args.get('id')
        returnClass = {}

        try:
            ourClass = Class.query.filter_by(classID=classID).first()

            if ourClass is None:
                return jsonify(succcess=False, message='There is no such class in the database')

            returnClass = {'id': int(ourClass.classID),
                           'letter': ourClass.classLetter,
                           'room': ourClass.classRoom,
                           'start': ourClass.classStart,
                           'name': str(ourClass.classStart) + ourClass.classLetter,
                           'pupils': [],
                           'professors': []
                           }

            altname = getClassAltName(ourClass.classStart, ourClass.classLetter)
            if altname != None:
                returnClass['altname'] = altname

            for professor in ourClass.profs:
                returnClass['professors'].append({'id': professor.profID, 'wholeName': '{} {}'.format(professor.profName, professor.profSurname)})

            for pupil in ourClass.pupils.order_by(Students.studentSurname).all():
                returnClass['pupils'].append({'id': pupil.studentID, 'name': pupil.studentName, 'surname': pupil.studentSurname})

            statusResponse = 1
        except:
            return jsonify(success=False, message='Error')

        return jsonify(success=True, rclass=returnClass)

    @classes_api.expect(newClass)
    @classes_api.doc(security='apikey')
    @token_required
    def post(self, tokenData):
        """ Adds a class to a database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to create classes")

        try:
            reJson = request.get_json()

            newClass = Class()
            newClass.classLetter = reJson['letter']
            newClass.classRoom = reJson['room']
            newClass.classStart = reJson['start']

            for pupilID in reJson['pupils']:
                try:
                    pupil = Students.query.filter_by(studentID=pupilID).first()
                    if pupil != None:
                        newClass.pupils.append(pupil)
                    else:
                        return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(pupilID))
                except:
                    return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(pupilID))

            # Adding his parents
            for professorID in reJson['professors']:
                try:
                    professor = Professor.query.filter_by(profID=professorID).first()
                    if professor is not None:
                        newClass.profs.append(professor)
                    else:
                        return jsonify(succcess=False, message="There is no professor with the ID {} in the database.".format(professorID))
                except:
                    return jsonify(succcess=False, message="There is no professor with the ID {} in the database.".format(parentID))

            db.session.add(newClass)
            db.session.commit()
            return jsonify(succcess=True, classID=newClass.classID)
        except:
            return jsonify(success=False, message='Not enought information provided')

    @classes_api.expect(idOnlyParserJson)
    @classes_api.doc(security='apikey')
    @token_required
    def delete(self, tokenData):
        """ Removes a class from a database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to delete classes")

        try:
            reJson = request.get_json()
            ourClass = Class.query.filter_by(classID=reJson['id']).first()

            deleteAllPupils(ourClass)
            deleteAllProfessors(ourClass)

            db.session.delete(ourClass)
            db.session.commit()
            return jsonify(succcess=True)
        except:
            raise
            return jsonify(success=False, message="Failed deleting")

    @classes_api.expect(updateClass)
    @classes_api.doc(security='apikey')
    @token_required
    def put(self, tokenData):
        """ Updates a class """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to update classes")

        try:
            reJson = request.get_json()
            ourClass = Class.query.filter_by(classID=reJson['id']).first()

            if 'letter' in reJson:
                ourClass.classLetter = reJson['letter']
            if 'room' in reJson:
                ourClass.classRoom = reJson['room']
            if 'start' in reJson:
                ourClass.classStart = reJson['start']

            print(reJson['professors'])

            # Adding his professors
            deleteAllProfessors(ourClass)
            for professorID in reJson['professors']:
                try:
                    professor = Professor.query.filter_by(profID=professorID).first()
                    if professor is not None:
                        ourClass.profs.append(professor)
                    else:
                        return jsonify(succcess=False, message="There is no professor with the ID {} in the database.".format(professorID))
                except:
                    return jsonify(succcess=False, message="There is no professor with the ID {} in the database.".format(parentID))

            deleteAllPupils(ourClass)
            for pupilID in reJson['pupils']:
                try:
                    pupil = Students.query.filter_by(studentID=pupilID).first()
                    ourClass.pupils.append(pupil)
                    print(ourClass.pupils[0].studentID)  # Quick fix, without this it doesn't work !!!
                except:
                    return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(pupilID))

            db.session.commit()
            return jsonify(succcess=True)
        except:
            return jsonify(success=False, message='fail')
