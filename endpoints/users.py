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

users_blueprint = Blueprint('user', __name__, url_prefix='/user')

@users_blueprint.route('/get_all', methods=['GET'])
def getUsers():
    if request.method=='GET':
        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['name'] = user.user_name
            user_data['email'] = user.email
            user_data['role'] = user.role
            user_data['contact'] = user.contact
            output.append(user_data)
        return jsonify({'users': output, 'message': 'success', 'status': '200'})
    
@users_blueprint.route('/get/<id>', methods=['GET'])
def getUser(id):
    if request.method=='GET':
        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message': 'No user found', 'status': '404'})
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.user_name
        user_data['email'] = user.email
        user_data['role'] = user.role
        user_data['contact'] = user.contact
        return jsonify({'user': user_data, 'message': 'success', 'status': '200'})

@users_blueprint.route('/delete/<id>', methods=['DELETE'])
def deleteUser(id):
    if request.method=='DELETE':
        if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
            return jsonify("Unauthorized"), 401
        cur_user = token_required_test(request.headers.get("Authorization"))
        if cur_user.role != 'admin':
            return jsonify({'message': 'You are not authorized to perform this action', 'status': '401'})
        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message': 'No user found', 'status': '404'})
        if user.role == 'admin':
            return jsonify({'message': 'You cannot delete an admin', 'status': '401'})
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted', 'status': '200'})

@users_blueprint.route('/update/<id>', methods=['PUT'])
def updateUser(id):
    if request.method=='PUT':
        if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
            return jsonify("Unauthorized"), 401
        cur_user = token_required_test(request.headers.get("Authorization"))
        if cur_user.id != id and cur_user.role != 'admin':
            return jsonify({'message': 'You are not authorized to perform this action', 'status': '401'})
        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({'message': 'No user found', 'status': '404'})
        changes = False
        if 'name' in request.json and request.json['name']:
            user.user_name = request.json['name']
            changes = True
        if 'email' in request.json and request.json['email']:
            user.email = request.json['email']
            changes = True

        if 'contact' in request.json and request.json['contact']:
            user.contact = request.json['contact']
            changes = True
        if 'role' in request.json and request.json['role']:
            user.role = request.json['role']
            changes = True
        if 'password' in request.json and request.json['password']:
            user.password = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            changes = True
        if not changes:
            return jsonify({'message': 'No changes made', 'status': '400'})
        db.session.commit()
        return jsonify({'message': 'User updated', 'status': '200'})
    return jsonify({'message': 'Method not allowed', 'status': '400'})