# Normal imports
from flask import Blueprint, request, jsonify
from flask_restplus import Api, Namespace, fields, Resource, reqparse
from datetime import date
from .helpers import deleteAllClasses
import os
import sys
import inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from core.sqlClasses import *
from core.helpers import token_required, getClassAltName

professors_api = Namespace('professors', 'Operations with professors')

# Setting up ID only parser
idOnlyParser = reqparse.RequestParser()
idOnlyParser.add_argument('id', type=int, required=True, location="args")

idOnlyParserJson = professors_api.model('DeleteEntry', {
    'id': fields.Integer(default=1, required=True)
})

# Setting up "First" parser
firstNArg = reqparse.RequestParser()
firstNArg.add_argument('first', type=int, required=False, location="args")

# Defining a newProfessor model
newProfessor = professors_api.model('NewProfessor', {
    'name': fields.String(default="John", required=True),
    'surname': fields.String(default="Doe", required=True),
    'email': fields.String(default="professor@mail.com", required=True),
    'loc': fields.String(default='1st floor', description="Location of professors office"),
    'adress': fields.String(default="Students Adress 16 NY", required=True),
    'phone': fields.String(default="+421 999 999 999", required=True),
    'classes': fields.List(fields.Integer, description="IDs of the classes")
})

# Defining a updateProfessor model
updateProfessor = professors_api.model('UpdateProfessor', {
    'id': fields.Integer(default=1, required=True),
    'name': fields.String(default="John", required=True),
    'surname': fields.String(default="Doe", required=True),
    'email': fields.String(default="professor@mail.com", required=True),
    'loc': fields.String(default='1st floor', description="Location of professors office"),
    'adress': fields.String(default="Students Adress 16 NY", required=True),
    'phone': fields.String(default="+421 999 999 999", required=True),
    'classes': fields.List(fields.Integer, description="IDs of the classes")
})


@professors_api.route('/all')
class AllProfessors(Resource):
    @professors_api.expect(firstNArg)
    def get(self):
        orderByArg = request.args.get('orderBy')
        orderedParents = []
        mainResponse = []
        firstN = None

        if 'first' in request.args:
            firstN = int(request.args['first'])

        if orderByArg == "id" or not orderByArg:
            orderedProfessors = Professor.query.order_by(Professor.profID).limit(firstN).all()
        elif orderByArg == "name":
            orderedProfessors = Professor.query.order_by(Professor.profName).limit(firstN).all()
        elif orderByArg == "surname":
            orderedProfessors = Professor.query.order_by(Professor.profSurname).limit(firstN).all()

        for professor in orderedProfessors:
            profR = {'id': professor.profID,
                     'name': professor.profName,
                     'surname': professor.profSurname,
                     'title': professor.profTitle,
                     'email': professor.profEmail,
                     'phone': professor.profPhone
                     }
            if len(professor.classes.all()) > 0:
                profR['class'] = professor.classes.first().classID
            else:
                profR['class'] = -1

            mainResponse.append(profR)

        return jsonify(success=True, professors=mainResponse)


@professors_api.route('')
class OneProfessor(Resource):
    """ Professor namespace """

    @professors_api.expect(idOnlyParser)
    def get(self):
        """ Returns a specific professor """
        profID = request.args.get('id')
        statusResponse = -1
        returnProfessor = {}

        try:
            professor = Professor.query.filter_by(profID=profID).first()

            returnProfessor = {
                'id': int(professor.profID),
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

    @professors_api.expect(newProfessor)
    @professors_api.doc(security='apikey')
    @token_required
    def post(self, tokenData):
        """ Adds a professor to a database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to create professors")

        try:
            professor = Professor()
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

    @professors_api.expect(idOnlyParserJson)
    @professors_api.doc(security='apikey')
    @token_required
    def delete(self, tokenData):
        """ Removes a professor from a database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to delete professors")

        try:
            reJson = request.get_json()
            professor = Professor.query.filter_by(profID=reJson['id']).first()

            deleteAllClasses(professor)

            db.session.commit()
            db.session.delete(professor)
            db.session.commit()
            return jsonify(succcess=True)
        except:
            raise
            return jsonify(success=False, message="There is no professor with the ID {} in the database.".format(reJson['id']))

    @professors_api.expect(updateProfessor)
    @professors_api.doc(security='apikey')
    @token_required
    def put(self, tokenData):
        """ Updates a professor in the database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to update professors")

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
            deleteAllClasses(professor)

            for classID in reJson['classes']:
                try:
                    newClass = Class.query.filter_by(classID=classID).first()
                    if newClass is not None:
                        professor.classes.append(newClass)
                    else:
                        return jsonify(success=False, message="There is no class with the ID {} in the database.".format(classID))
                except:
                    return jsonify(success=False, message="There is no class with the ID {} in the database.".format(classID))

            db.session.commit()
            return jsonify(succcess=True, professorID=professor.profID)
        except:
            return jsonify(success=False, message='Fail')
