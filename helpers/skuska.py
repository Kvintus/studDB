from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../assets/skuska.db'
db = SQLAlchemy(app)

subs = db.Table('subs',
    db.Column('user_id', db.Integer, db.ForeignKey('user.userID')),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.channelID'))
)

class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    subscriptions = db.relationship('Channel', secondary=subs, backref=db.backref('subscribers', lazy='dynamic'))

class Channel(db.Model):
    channelID = db.Column(db.Integer, primary_key=True)
    channelName = db.Column(db.String(20))
    susbTo = db.relationship('User', secondary=subs, backref=db.backref('channels', lazy='dynamic'))