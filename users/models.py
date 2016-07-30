from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    birthdate = db.Column('birthdate', db.Date)
    account_value = db.Column('account_value', db.Float)
    address = db.Column('address', db.String)
    hiredate = db.Column('hiredate', db.Date, default=datetime.utcnow)
    state = db.Column(db.Integer, db.ForeignKey('states.id'))

    def __repr__(self):
        return '<User %r>' % (self.name)


class States(db.Model):
    __tablename__ = "states"

    id = db.Column('id', db.Integer, primary_key=True)
    state_full = db.Column('state_full', db.String)