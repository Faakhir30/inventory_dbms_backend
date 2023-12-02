from flask import Blueprint, request, jsonify
from main import db
from models.user import Admin, Customer, Supplier
from sqlalchemy.exc import IntegrityError
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
            # Creating the user object
            if role == 'admin':
                new_user = Admin(user_name=name, email=email, password=password, contact=contact)
            elif role == 'customer':
                new_user = Customer(user_name=name, email=email, password=password, contact=contact)
            elif role == 'supplier':
                new_user = Supplier(user_name=name, email=email, password=password, contact=contact)
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
            # Extracting details from the request
            email = request.json['email']
            password = request.json['password']
            role = request.json['role']
            # Creating the user object
            if role == 'admin':
                user = Admin.query.filter_by(email=email).first()
            elif role == 'customer':
                user = Customer.query.filter_by(email=email).first()
            elif role == 'supplier':
                user = Supplier.query.filter_by(email=email).first()
            else:
                return jsonify({'error': 'Invalid role'}), 400

            # Checking if the user exists
            if user is None:
                return jsonify({'error': 'Invalid email or password'}), 400

            # Checking if the password is correct
            if user.password != password:
                return jsonify({'error': 'Invalid email or password'}), 400

            # Creating the response object
            response = {
                'message': 'User logged in successfully',
                'data': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'contact': user.contact,
                    'role': role
                }
            }
            return jsonify(response), 200

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500