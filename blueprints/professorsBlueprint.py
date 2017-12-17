# Normal imports 
from flask import Blueprint, request, jsonify
from datetime import date
import os,sys,inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from helpers.sqlClasses import Professor

professors_mod = Blueprint('professors', __name__)

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

@professors_mod.route('/')
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

@professors_mod.route('/getOne')
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

##                       Professor manipulation                            ##
@professors_mod.route('/add', methods = ['POST'])
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

@professors_mod.route('/remove', methods = ['POST'])
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

@professors_mod.route('/update', methods = ['POST'])
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