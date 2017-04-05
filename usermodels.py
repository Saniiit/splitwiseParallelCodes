from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test3.db'
#db = SQLAlchemy(app)
class User(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    bills = db.Column(db.Integer)
    balance = db.Column(db.Integer)

    def __init__(self, name, email, password, bills, balance):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.bills = bills
        self.balance = balance

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
            'email': self.email,
            'bills' : self.bills,
            'balance' : self.balance,
        }

    def __repr__(self):
        return "User<%d> :%s :: %s,Balance :%s" %(self.id, self.name,self.email,self.balance)

db.create_all()
