from flask_sqlalchemy import SQLAlchemy
from app import db

class Transaction(db.Model):
    __tablename__ = 'transaction_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(255))
    amount = db.Column(db.Integer)
    majorSplit = db.Column(db.String(255))
    split_amongst = db.Column(db.String(255))
    status = db.Column(db.Integer)

    def __init__(self, description, amount, majorSplit, split_amongst, status):
        self.description = description
        self.amount = amount
        self.majorSplit = majorSplit
        self.split_amongst = split_amongst
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'majorSplit': self.majorSplit,
            'split_amongst': self.split_amongst,
            'status': self.status,
        }

    def __repr__(self):
        return "Transaction<%d>: %s;Amount:%s;%s,%s" %(self.id, self.description,self.amount,self.majorSplit,self.split_amongst)

db.create_all()
