from flask import Blueprint, request, session, jsonify
from app import db, requires_auth
from .models import Transaction

#from validate_email import validate_email
mod_transaction = Blueprint('transaction', __name__, url_prefix='/api')
@mod_transaction.route('/transaction', methods=['POST'])
@requires_auth
def create_bill():

    description = request.form['description']
    amount = request.form['amount']
    majorSplit = request.form['majorSplit']
    split_amongst = request.form['split_amongst']
    status = False

    transaction = Transaction(description, amount, majorSplit, split_amongst, status)
    db.session.add(transaction)
    db.session.commit()
    return jsonify(success=True, transaction = transaction.to_dict())

#@mod_transaction.route('/transaction/<id>', methods=['POST'])
#@requires_auth
#def edit_bill(id):

#    user_id = session['user_id']
#    transaction = Transaction.query.filter(Transaction.id == id, Transaction.user_id == user_id).first()
#    if transaction is None:
#        return jsonify(success=False), 404
#    else:
#        transaction.description = request.form['description']
#        transaction.amount = request.form['amount']
#        transaction.majorSplit = request.form['majorSplit']
#        transaction.split_amongst = request.form['split_amongst']
#        db.session.commit()
#        return jsonify(success=True)

@mod_transaction.route('/transaction/<id>/settle-up', methods=['POST'])
@requires_auth
def settle_bill(id):

    user_id = session['user_id']
    transaction = Transaction.query.filter(Transaction.id == id, Transaction.user_id == user_id).first()
#* updating the balance ???????
    if transaction is None:
        return jsonify(success=False), 404
    else:
db.session.delete(transaction)  #* can we just not delete the table in the transaction_table--------- for settling up
        # need to update the status
        db.session.commit()
        return jsonify(success=True)

@mod_transaction.route('/transaction/<id>/delete', methods=['POST'])
@requires_auth
def delete_bill(id):

    user_id = session['user_id']
    transaction = Transaction.query.filter(Transaction.id == id, Transaction.user_id == user_id).first()
    if transaction is None:
        return jsonify(success=False), 404
    else:
        db.session.delete(transaction)
        db.session.commit()
        return jsonify(success=True)
