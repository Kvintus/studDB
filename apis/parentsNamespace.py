# Normal imports
from flask import request, jsonify
from flask_restplus import Api, Namespace, fields, Resource, reqparse
import os
import sys
import inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from core.sqlClasses import *
from core.helpers import token_required

parents_api = Namespace('parents', 'Operation with parents')

# Setting up ID only parser
idOnlyParser = reqparse.RequestParser()
idOnlyParser.add_argument('id', type=int, required=True, location="args")


# Setting up "First" parser
firstNArg = reqparse.RequestParser()
firstNArg.add_argument('first', type=int, required=False, location="args")


idOnlyParserJson = parents_api.model('DeleteEntry', {
    'id': fields.Integer(default=1, required=True)
})

# Defining a newParent model
newParent = parents_api.model('NewParent', {
    'name': fields.String(default="John", required=True),
    'surname': fields.String(default="Doe", required=True),
    'email': fields.String(default="students@mail.com", required=True),
    'adress': fields.String(default="Students Adress 16 NY", required=True),
    'phone': fields.String(default="+421 999 999 999", required=True),
    'children': fields.List(fields.Integer, description="Children IDs")
})

# Defining a updateParent model
updateParent = parents_api.model('UpdateParent', {
    'id': fields.Integer(default=0, required=True),
    'name': fields.String(default="John", required=True),
    'surname': fields.String(default="Doe", required=True),
    'email': fields.String(default="students@mail.com", required=True),
    'adress': fields.String(default="Students Adress 16 NY", required=True),
    'phone': fields.String(default="+421 999 999 999", required=True),
    'children': fields.List(fields.Integer, description="Children IDs")
})


@parents_api.route('/all')
class AllParents(Resource):
    @parents_api.expect(firstNArg)
    def get(self):
        """ Returns all the parents """
        orderByArg = request.args.get('orderBy')
        statusResponse = -1
        orderedParents = []
        mainResponse = []
        firstN = None

        if 'first' in request.args:
            firstN = int(request.args['first'])

        if orderByArg == "id" or not orderByArg:
            orderedParents = Parent.query.order_by(Parent.parentID).limit(firstN).all()
            statusResponse = 1
        elif orderByArg == "name":
            orderedParents = Parent.query.order_by(Parent.parentName).limit(firstN).all()
            statusResponse = 1
        elif orderByArg == "surname":
            orderedParents = Parent.query.order_by(Parent.parentSurname).first(firstN).all()
            statusResponse = 1

        for parent in orderedParents:
            mainResponse.append({'id': parent.parentID,
                                 'name': parent.parentName,
                                 'surname': parent.parentSurname,
                                 'email': parent.parentEmail,
                                 'phone': parent.parentPhone
                                 })

        return jsonify(success=True, parents=mainResponse)


@parents_api.route('')
class oneParent(Resource):
    """ Parent namespace """

    @parents_api.expect(idOnlyParser)
    def get(self):
        """ Returns one parent """
        if request.method == 'GET':
            parentID = request.args.get('id')
            statusResponse = -1
            returnParent = {}

            parent = Parent.query.filter_by(parentID=parentID).first()
            if parent == None:
                return jsonify(success=False, message='There is no such parent in the database')

            returnParent = {'id': int(parent.parentID),
                            'name': parent.parentName,
                            'surname': parent.parentSurname,
                            'email': parent.parentEmail,
                            'adress': parent.parentAdress,
                            'phone': parent.parentPhone,
                            'children': []
                            }

            for child in parent.children:
                ourChild = {'id': child.studentID, 'wholeName': '{} {}'.format(child.studentName, child.studentSurname)}
                returnParent['children'].append(ourChild)

            statusResponse = 1

        return jsonify(succcess=True, parent=returnParent)

    @parents_api.expect(newParent)
    @parents_api.doc(security='apikey')
    @token_required
    def post(self, tokenData):
        """ Adds a parent to a database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to create parents")

        try:
            parent = Parent()
            reJson = request.get_json()

            parent.parentEmail = reJson['email']
            parent.parentName = reJson['name']
            parent.parentPhone = reJson['phone']
            parent.parentSurname = reJson['surname']
            parent.parentAdress = reJson['adress']

            # Adding his parents
            for childID in reJson['children']:
                try:
                    child = Students.query.filter_by(studentID=childID).first()
                    parent.children.append(child)
                    print(parent.children[0].studentID)  # Quick fix, without this it doesn't work !!!
                except:
                    return jsonify(succcess=False, message="There is no parent with the ID {} in the database.".format(childID))

            db.session.add(parent)
            db.session.commit()
            return jsonify(succcess=True, parentID=parent.parentID)
        except:
            return jsonify(success=False)

    @token_required
    @parents_api.doc(security='apikey')
    @parents_api.expect(idOnlyParserJson)
    def delete(self, tokenData):
        """ Removes a parent from a database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to delete parents")

        try:
            reJson = request.get_json()
            parent = Parent.query.filter_by(parentID=reJson['id']).first()

            parent.children = []

            db.session.commit()
            db.session.delete(parent)
            db.session.commit()
            return jsonify(succcess=True)
        except:
            return jsonify(success=False)

    @token_required
    @parents_api.doc(security='apikey')
    @parents_api.expect(updateParent)
    def put(self, tokenData):
        """ Updates a parent in the database """

        if tokenData['privilege'] < 3:
            return jsonify(succcess=False, message="You don't have privilege to update parents")

        try:
            reJson = request.get_json()

            # Find the student to update
            try:
                parent = Parent.query.filter_by(parentID=int(reJson['id'])).first()
            except:
                return jsonify(succcess=False, message="There is no parent with the ID {} in the database.".format(reJson['id']))

            # Update
            if 'email' in reJson:
                parent.parentEmail = reJson['email']
            if 'name' in reJson:
                parent.parentName = reJson['name']
            if 'phone' in reJson:
                parent.parentPhone = reJson['phone']
            if 'surname' in reJson:
                parent.parentSurname = reJson['surname']
            if 'start' in reJson:
                parent.parentStart = reJson['start']
            if 'adress' in reJson:
                parent.parentAdress = reJson['adress']

            # Adding his children
            for child in parent.children:
                parent.children.remove(child)

            for childID in reJson['children']:
                try:
                    child = Students.query.filter_by(studentID=childID).first()
                    parent.children.append(child)
                    print(parent.children[0].studentID)  # Quick fix, without this it doesn't work !!!
                except:
                    raise
                    return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(childID))

            db.session.commit()
            return jsonify(success=True, parentName="{} {}".format(parent.parentName, parent.parentSurname))
        except:
            raise
            return jsonify(success=False)
