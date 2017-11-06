from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../assets/database.db'
db = SQLAlchemy(app)

#Asociation tables
relParentChild = db.Table('relParentChild',
    db.Column('parentID', db.Integer, db.ForeignKey('Parents.parentID')),
    db.Column('childID', db.Integer, db.ForeignKey('Students.studentID'))
)

relClassStudent = db.Table('relClassStudent',
    db.Column('classID', db.Integer, db.ForeignKey('Classes.classID')),
    db.Column('studentID', db.Integer, db.ForeignKey('Students.studentID'))    
)

relClassProf = db.Table('relClassProf', 
    db.Column('classID', db.Integer, db.ForeignKey('Classes.classID')),
    db.Column('profID', db.Integer, db.ForeignKey('Professors.profID'))
)



#main Classes / Tables
class Professor(db.Model):
    __tablename__ = 'Professors'

    #Basic info
    profID = db.Column(db.Integer, primary_key=True)
    profTitle = db.Column(db.String(80), nullable=True)
    profName = db.Column(db.String(50), nullable=False)
    profSurname = db.Column(db.String(80), nullable=False)
    profLoc = db.Column(db.String(10))
    profEmail = db.Column(db.String(50), nullable=False)
    profPhone = db.Column(db.String(20), nullable=False) #not setting it to unique=True so I can ganarete them randomly
    profAdress = db.Column(db.String(80))

    #Relationships
    classRel = db.relationship('Class', secondary=relClassProf, backref=db.backref('profs', lazy='dynamic'))

    def __repr__(self):
        return '<Professor %r>' % self.profSurname

class Parent(db.Model):
    __tablename__ = 'Parents'
    
    #Basic info
    parentID = db.Column(db.Integer, primary_key=True, nullable=False)
    parentName = db.Column(db.String(50), nullable=False)
    parentSurname = db.Column(db.String(50), nullable=False)
    parentEmail = db.Column(db.String(50), nullable=False)
    parentPhone = db.Column(db.String(20), nullable=False)
    parentAdress = db.Column(db.String(80))

    #Relationships
    childrenRel = db.relationship('Students', secondary=relParentChild, backref=db.backref('parents', lazy='dynamic'))

class Students(db.Model):
    __tablename__ = 'Students'
    
    #Basic Info
    studentID = db.Column(db.Integer, primary_key = True)
    studentName = db.Column(db.String(50),nullable=False)
    studentSurname = db.Column(db.String(50), nullable=False)
    studentDateOfBirth = db.Column(db.String(12), nullable=False)
    studentStart = db.Column(db.Integer , nullable=False)
    studentAdress = db.Column(db.String(80))
    studentEmail = db.Column(db.String(80))
    studentPhone = db.Column(db.String(20))
    
    #Ralationships
    classRel = db.relationship('Class', secondary=relClassStudent, backref=db.backref('pupils', lazy='dynamic'))
    parentsRel = db.relationship('Parent', secondary= relParentChild,backref=db.backref('children', lazy='dynamic'))

class Class(db.Model):
    __tablename__ = 'Classes'
    classID = db.Column(db.Integer, primary_key=True)
    classLetter = db.Column(db.String(2))
    classRoom = db.Column(db.String(20))
    classStart = db.Column(db.Integer, nullable = False)
    
    #Relationships
    profRel = db.relationship('Professor', secondary=relClassProf, backref=db.backref('classes', lazy='dynamic'))
    pupilsRel = db.relationship('Students', secondary=relClassStudent, backref=db.backref('classes', lazy='dynamic'))