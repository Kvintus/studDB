# Normal imports 
from flask import Blueprint, request, jsonify
import os,sys,inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from helpers.sqlClasses import Parent

parents_mod = Blueprint('parents', __name__)

@parents_mod.route('/')
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
                                    'surname': parent.parentSurname,
                                    'email': parent.parentEmail,
                                    'phone': parent.parentPhone
                                    })
        
        return jsonify(status = statusResponse, parents = mainResponse)
            
@parents_mod.route('/getOne')
def getParent():
    if request.method == 'GET':
        parentID = request.args.get('id')
        statusResponse = -1
        returnParent = {}
        
        try:
            parent = Parent.query.filter_by(parentID = parentID).first()

            if parent is None:
                return jsonify(status=-1, message='There is no such parent in the database')
            
            returnParent = {'id': int(parent.parentID),
                                    'name': parent.parentName,
                                    'surname': parent.parentSurname,
                                    'email': parent.parentEmail,
                                    'adress': parent.parentAdress,
                                    'phone': parent.parentPhone,
                                    'children': []
                                    }
            
            for child in parent.children:
                ourChild = {'id':child.studentID, 'wholeName':'{} {}'.format(child.studentName, child.studentSurname)}
                returnParent['children'].append(ourChild)
    
            statusResponse = 1
        except:
            raise
            statusResponse = -1

        return jsonify(status=statusResponse, parent=returnParent)

##                       Parent manipulation                            ##
@parents_mod.route('/add', methods = ['POST'])
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

        # Adding his parents
        for childID in reJson['children']:
            try:
                child = Students.query.filter_by(studentID=childID).first()
                parent.children.append(child)
                print(parent.children[0].studentID) #Quick fix, without this it doesn't work !!!
            except:
                raise
                return jsonify(succcess=False, message="There is no parent with the ID {} in the database.".format(childID))

        db.session.add(parent)
        db.session.commit()
        return jsonify(succcess=True, parentID=parent.parentID)
    except:
        return jsonify(success=False)

@parents_mod.route('/remove', methods = ['POST'])
def removeParent():
    """ Removes a parent from a database """    
    
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

@parents_mod.route('/update', methods = ['POST'])
def updateParent():
    """ Updates a parent in the database """    
    
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
                print(parent.children[0].studentID) #Quick fix, without this it doesn't work !!!
            except:
                raise
                return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(childID))
        

        
        db.session.commit() 
        return jsonify(success=True, parentName="{} {}".format(parent.parentName, parent.parentSurname))
    except:
        raise
        return jsonify(success=False)