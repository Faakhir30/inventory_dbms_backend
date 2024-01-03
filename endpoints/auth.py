from email.mime import image
from flask import Blueprint, request, jsonify
from dependencies.authentication import token_required_test
from main import db
from models.user import Admin, Customer, Supplier, User, Employee
from sqlalchemy.exc import IntegrityError
import bcrypt
import jwt
import os
import datetime
secret_key = os.getenv("SECRET_KEY")

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@auth_blueprint.route('/signup', methods=['POST'])
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
            image = request.json['image']
            # Creating the user object
            if role == 'admin':
                new_user = Admin(user_name=name, email=email, password=hashed_password, contact=contact)
                
            elif not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify("Unauthorized"), 401

            elif role == 'customer':
                new_user = Customer(user_name=name, email=email, password=hashed_password, contact=contact, image=image)
            elif role == 'supplier':
                new_user = Supplier(user_name=name, email=email, password=hashed_password, contact=contact, image=image)
            elif role == 'employee':
                new_user = Employee(user_name=name, email=email, password=hashed_password, contact=contact, image=image)
            else:
                return jsonify({'message': 'Invalid role', 'status':400}), 400

            # Adding the user to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully', "status":201}), 201

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'message': error_info, 'status':500}), 500
        except TypeError as e:
            return jsonify({'message': str(e), 'status':400}), 400
        
@auth_blueprint.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.json['email']
            password = request.json['password']
            user = User.query.filter_by(email=email).first()
            if user is None:
                return jsonify({'message': 'Invalid email or password', 'status':400}), 400
            hashed_password = user.password
            if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return jsonify({'message': 'Invalid email or password', 'status':400}), 400

            # Creating the response object
            response = {
                'message': 'User logged in successfully',
                'data': {
                    'id': user.id,
                    'name': user.user_name,
                    'email': user.email,
                    'contact': str(user.contact),
                    'role': user.role,
                    'image': user.image,
                    'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
            token = jwt.encode(response["data"], secret_key, algorithm='HS256')
            response['data'].pop('created_at')
            response['data']['token'] = token
            response['status'] = 200
            return jsonify(response), 200

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'message': error_info}), 500