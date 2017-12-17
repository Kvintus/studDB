# Normal imports 
from flask import Blueprint, request, jsonify
from datetime import date
import os,sys,inspect

# Importin from parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from helpers.sqlClasses import Class

# Creating blueprint
classes_mod = Blueprint('classes', __name__)

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

@classes_mod.route('/')
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
        return jsonify(status=statusResponse, classes=mainResponse)

@classes_mod.route('/getOne')
def getClass():
    if request.method == 'GET':
        classID = request.args.get('id')
        statusResponse = -1
        returnClass = {}
        
        try:
            ourClass = Class.query.filter_by(classID = classID).first()

            if ourClass is None:
                return jsonify(status=-1, message='There is no such class in the database')
            
            returnClass = {'id': int(ourClass.classID),
                            'letter': ourClass.classLetter,
                            'room': ourClass.classRoom,
                            'start': ourClass.classStart,
                            'name': str(ourClass.classStart) + ourClass.classLetter,
                            'pupils': [],
                            'professors' : []
                                    }

            altname = getClassAltName(ourClass.classStart, ourClass.classLetter)
            if altname != None:
                returnClass['altname'] = altname

            for professor in ourClass.profs:
                returnClass['professors'].append({'id': professor.profID, 'wholeName': '{} {}'.format(professor.profName, professor.profSurname)})
            
            for pupil in ourClass.pupils.order_by(Students.studentSurname).all():
                returnClass['pupils'].append({'id':pupil.studentID, 'name': pupil.studentName, 'surname': pupil.studentSurname})

            statusResponse = 1
        except:
            statusResponse = -1

        return jsonify(status=statusResponse, rclass=returnClass)

##                       Manipulation                            ##
@classes_mod.route('/add', methods = ['POST'])
def addClass():
    """ Adds a class to a database """    
    
    try:
        reJson = request.get_json()

        newClass =  Class()
        newClass.classLetter = reJson['letter']
        newClass.classRoom = reJson['room']
        newClass.classStart = reJson['start']

        for pupilID in reJson['pupils']:
            try:
                pupil = Students.query.filter_by(studentID=pupilID).first()
                if pupil is not None:
                    newClass.pupils.append(pupil)
                    print(newClass.pupils[0].studentID) #Quick fix, without this it doesn't work !!!
                else:
                    return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(pupilID))
            except:
                raise
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
                raise
                return jsonify(succcess=False, message="There is no professor with the ID {} in the database.".format(parentID))
        


        db.session.add(newClass)
        db.session.commit()
        return jsonify(succcess=True, classID=newClass.classID)
    except:
        raise
        return jsonify(success=False, message='Not enought information provided')

@classes_mod.route('/remove', methods = ['POST'])
def removeClass():
    """ Removes a class from a database """    
     
    try:
        reJson = request.get_json()
        ourClass = Class.query.filter_by(classID=reJson['id']).first()

        ourClass.pupils = []
        ourClass.profs = []

        db.session.commit()
        db.session.delete(ourClass)
        db.session.commit()
        return jsonify(succcess=True)
    except:
        return jsonify(success=False, message="Failed deleting")

@classes_mod.route('/update', methods = ['POST'])
def updateClass():
    """ Updates a class """    
    
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
        ourClass.profs = []
        for professorID in reJson['professors']:
            try:
                professor = Professor.query.filter_by(profID=professorID).first()
                if professor is not None:
                    ourClass.profs.append(professor)
                else:
                    return jsonify(succcess=False, message="There is no professor with the ID {} in the database.".format(professorID))
            except:
                raise
                return jsonify(succcess=False, message="There is no professor with the ID {} in the database.".format(parentID))

        ourClass.pupils = []
        for pupilID in reJson['pupils']:
            try:
                pupil = Students.query.filter_by(studentID=pupilID).first()
                ourClass.pupils.append(pupil)
                print(ourClass.pupils[0].studentID) #Quick fix, without this it doesn't work !!!
            except:
                raise
                return jsonify(succcess=False, message="There is no student with the ID {} in the database.".format(pupilID))


        db.session.commit()
        return jsonify(succcess=True)
    except:
        raise
        return jsonify(success=False, message='fail')