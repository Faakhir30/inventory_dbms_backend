from flask import Blueprint, request, jsonify
from main import db
from models.user import Admin, Customer, Supplier, User
from sqlalchemy.exc import IntegrityError
import bcrypt
import jwt
import os
secret_key = os.getenv("SECRET_KEY")

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/user/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        try:
            # Extracting details from the request
            name = request.json['name']
            email = request.json['email']
            password = request.json['password']
            contact = request.json['contact']
            role = request.json['role']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Creating the user object
            if role == 'admin':
                new_user = Admin(user_name=name, email=email, password=hashed_password, contact=contact)
            elif role == 'customer':
                new_user = Customer(user_name=name, email=email, password=hashed_password, contact=contact)
            elif role == 'supplier':
                new_user = Supplier(user_name=name, email=email, password=hashed_password, contact=contact)
            else:
                return jsonify({'error': 'Invalid role'}), 400

            # Adding the user to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400
        
@auth_blueprint.route('/user/signin', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.json['email']
            password = request.json['password']
            user = User.query.filter_by(email=email).first()
            if user is None:
                return jsonify({'error': 'Invalid email or password'}), 400
            hashed_password = user.password
            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return jsonify({'error': 'Invalid email or password'}), 400

            # Creating the response object
            response = {
                'message': 'User logged in successfully',
                'data': {
                    'id': user.id,
                    'name': user.user_name,
                    'email': user.email,
                    'contact': str(user.contact),
                    'role': user.role
                }
            }
            token = jwt.encode(response["data"], secret_key, algorithm='HS256')
            response['data']['token'] = token
            return jsonify(response), 200

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500