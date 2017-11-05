from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../assets/database.db'
db = SQLAlchemy(app)


class Professor(db.Model):
    __tablename__ = 'Professors'
    profID = db.Column(db.Integer, primary_key=True)
    profTitle = db.Column(db.String(80), nullable=False)
    profName = db.Column(db.String(50), nullable=False)
    profSurname = db.Column(db.String(80), nullable=False)
    profLoc = db.Column(db.String(10))
    profEmail = db.Column(db.String(50), nullable=False)
    profPhone = db.Column(db.String(20), nullable=False)
    profAdress = db.Column(db.String(80))

    def __repr__(self):
        return '<Professor %r>' % self.profSurname

class Parent(db.Model):
    __tablename__ = 'Parents'
    parentID = db.Column(db.Integer, primary_key=True, nullable=False)
    #TODO
    parentChildID = db.Column(db.Integer, )
    parentName = db.Column(db.String(50), nullable=False)
    parentSurname = db.Column(db.String(50), nullable=False)
    parentEmail = db.Column(db.String(50), nullable=False, unique=True)
    parentPhone = db.Column(db.String(20), nullable=False, unique=True)
    parentAdress = db.Column(db.String(80))

class Students(db.Model):
    __tablename__ = 'Students'
    studentID = db.Column(db.Integer, primary_key = True)
    studentName = db.Column(db.String(50),nullable=False)
    studentSurname = db.Column(db.String(50), nullable=False)
    #TODO Class
    studentDateOfBirth = db.Column(db.String(12), nullable=False)
    studentStart = db.Column(db.String(12), nullable=False)
    studentAdress = db.Column(db.String(80))
    studentEmail = db.Column(db.String(80), unique=True)
    studentPhone = db.Column(db.String(20), unique=True)

class Class(db.Model):
    __tablename__ = 'Classes'
    classID = db.Column(db.Integer, primary_key=True)
    className = db.Column(db.String(20))
    #TODO prof
    classRoom = db.Column(db.String(20))