from flask import Blueprint, request, session, jsonify
from sqlalchemy.exc import IntegrityError
from app import db
from .models import User
from .transaction.models import Transaction
from .transaction.controllers import Transaction

mod_user = Blueprint('user', __name__, url_prefix='/api')
#mod_user is an instance of Blueprint class. You can have several such instances across
#your project.

@mod_user.route('/login', methods=['GET'])
def check_login():
    if 'user_id' in session:
        user = User.query.filter(User.id == session['user_id']).first()
        return jsonify(success=True, user=user.to_dict())

    return jsonify(success=False), 401


@mod_user.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except Key1Error as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    user = User.query.filter(User.email == email).first()
    if user is None or not user.check_password(password):
        return jsonify(success=False, message="Invalid Credentials"), 400

    session['user_id'] = user.id
    #Notice this is how we login the user, by adding his id to the session dictionary.

    return jsonify(success=True, user=user.to_dict())

@mod_user.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id')
    return jsonify(success=True)

@mod_user.route('/signup', methods=['POST'])
def create_user():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    if '@' not in email:
        return jsonify(success=False, message="Please enter a valid email"), 400
    
    u = User(name, email, password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This email already exists"), 400

    return jsonify(success=True)

@mod_user.route('/allbills',method=['GET'])
def get_all_bills():
    userid = session['user_id']
    transaction = Transaction.query.filter(eval(Transaction.split_amongst)[0] == userid).all()
    for i in transaction:
        if i is None:
            return jsonify(success=False), 404
        else:
            if i.status is 0:
                return jsonify(success=True, message="You contributed %s towards the bill %s \n" %(i.split_amongst ?? ,i.description))
            else:
                return jsonify(success=True, message="%s bill has been settled \n" %(i.description))
