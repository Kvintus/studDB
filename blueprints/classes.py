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