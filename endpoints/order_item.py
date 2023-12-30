from flask import Blueprint, request, jsonify
from main import db
from models.user import Employee
from models.product import Product
from models.order import Orders, OrderItem
from sqlalchemy.exc import IntegrityError
from dependencies.authentication import token_required_test
from utils.general import object_as_dict
import datetime

order_item_blueprint = Blueprint('order_item', __name__, url_prefix='/order_item')

@order_item_blueprint.route('/get_all', methods=['GET'])
def get():
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            order_items = OrderItem.query.all()
            return jsonify({"order_items":[object_as_dict(order_item) for order_item in order_items], "status":200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@order_item_blueprint.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            order_item = OrderItem.query.filter_by(id=id).first()
            return jsonify({"order_item":object_as_dict(order_item), "status":200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@order_item_blueprint.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not request.headers.get("Authorization") or not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            # Extracting details from the request
            order_id = request.json['order_id']
            product_id = request.json['product_id']
            quantity = request.json['quantity']
            new_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity, unit_price= Product.query.filter_by(id=product_id).first().sale_price)
            db.session.add(new_order_item)
            db.session.commit()
            return jsonify({'message': 'OrderItem created successfully', 'status':200}), 201

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400
        
@order_item_blueprint.route('/update/<int:id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not request.headers.get("Authorization") or not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            order_item = OrderItem.query.filter_by(id=id).first()
            order_item.order_id = request.json['order_id']
            order_item.product_id = request.json['product_id']
            order_item.quantity = request.json['quantity']
            order_item.unit_price = request.json['unit_price']
            db.session.commit()
            return jsonify({'message': 'OrderItem updated successfully', 'status':200}), 200
        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400
        
@order_item_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not request.headers.get("Authorization") or not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            order_item = OrderItem.query.filter_by(id=id).first()
            db.session.delete(order_item)
            db.session.commit()
            return jsonify({'message': 'OrderItem deleted successfully', 'status':200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500