from flask import Blueprint, request, session, jsonify
from app import db, requires_auth
from .models import Transaction

mod_transaction = Blueprint('transaction', __name__, url_prefix='/api')
@mod_transaction.route('/transaction', methods=['POST'])
@requires_auth
def create_bill():

    description = request.form['description']
    amount = request.form['amount']
    majorSplit = request.form['majorSplit']
    split_amongst = request.form['split_amongst']
    status = 0

    transaction = Transaction(description, amount, majorSplit, split_amongst, status)
    db.session.add(transaction)
    db.session.commit()
    return jsonify(success=True, transaction = transaction.to_dict())

@mod_transaction.route('/transaction/<id>/settle-up', methods=['POST'])
@requires_auth
def settle_bill(id):

    transaction = Transaction.query.filter(Transaction.id == id).all()
    if transaction is None:
        return jsonify(success=False), 404
    else:
        transaction.status = 1
        db.session.commit()
        return jsonify(success=True, transaction = transaction.to_dict())

@mod_transaction.route('/transaction/<id>/delete', methods=['POST'])
@requires_auth
def delete_bill(id):

    transaction = Transaction.query.filter(Transaction.id == id).all()
    if transaction is None:
        return jsonify(success=False), 404
    else:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify(success=True)
