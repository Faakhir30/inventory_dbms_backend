from flask import Blueprint, request, jsonify
from models.transaction import Invoice
from main import db
from models.user import Employee
from models.product import Product
from models.order import Orders, OrderItem
from sqlalchemy.exc import IntegrityError
from dependencies.authentication import token_required_test
from utils.general import object_as_dict
import datetime

order_blueprint = Blueprint('order', __name__, url_prefix='/order')

@order_blueprint.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not request.headers.get("Authorization") or not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            # Extracting details from the request
            product_id = request.json['product_id']
            quantity = request.json['quantity']
            customer_id = cur_user.id
            if 'customer_id' in request.json:
                customer_id = request.json['customer_id']
            employees = Employee.query.all()
            orders = Orders.query.all()
            if not employees:
                return jsonify({'error': 'No employee found'}), 400
            most_free_emp_id = employees[0].id
            most_free_emp_order_count = len([order for order in orders if order.emp_id == most_free_emp_id])
            for emp in employees:
                emp_order_count = len([order for order in orders if order.emp_id == emp.id])
                if emp_order_count <= most_free_emp_order_count:
                    most_free_emp_id = emp.id
                    most_free_emp_order_count = emp_order_count
            if not most_free_emp_id:
                return jsonify({'error': 'No employee found'}), 400
            new_order = Orders(cust_id=customer_id, ordered_date=datetime.datetime.now(), emp_id=most_free_emp_id)      
            total = int(quantity) * Product.query.filter_by(id=product_id).first().sale_price
            db.session.add(new_order)
            db.session.commit()
            new_transaction = Invoice(order_id=new_order.id, total=total, user_id=customer_id)
            db.session.add(new_transaction)
            db.session.commit()
            for product_id, quantity in zip(product_id, quantity):
                new_order_item = OrderItem(order_id=new_order.id, product_id=product_id, quantity=quantity, unit_price=Product.query.filter_by(id=product_id).first().sale_price)
                db.session.add(new_order_item)
                db.session.commit()
            return jsonify({'message': 'Order created successfully', 'status':200}), 201

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400
        
@order_blueprint.route('/get_all', methods=['GET'])
def get():
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            orders = Orders.query.all()
            return jsonify({"orders":[object_as_dict(order) for order in orders], "status":200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@order_blueprint.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            order = Orders.query.filter_by(id=id).first()
            return jsonify(object_as_dict(order)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@order_blueprint.route('/get_by_customer/<int:id>', methods=['GET'])
def get_by_customer(id):
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            orders = Orders.query.filter_by(customer_id=id).all()
            for order in orders:
                order.order_items = OrderItem.query.filter_by(order_id=order.id).all()
            return jsonify([object_as_dict(order) for order in orders]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@order_blueprint.route('/get_by_employee/<int:id>', methods=['GET'])
def get_by_employee(id):
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            orders = Orders.query.filter_by(emp_id=id).all()
            return jsonify([object_as_dict(order) for order in orders]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@order_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            order = Orders.query.filter_by(id=id).first()
            if not order:
                return jsonify({'error': 'Order not found'}), 404
            transaction = Invoice.query.filter_by(order_id=id).first()
            db.session.delete(transaction)
            db.session.delete(order)
            db.session.commit()
            return jsonify({'message': 'Order deleted successfully', 'status':200}), 200
        except Exception as e:
            raise e
            return jsonify({'error': str(e)}), 500
        
@order_blueprint.route('/update/<int:id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not request.headers.get("Authorization") or not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            order = Orders.query.filter_by(id=id).first()
            if not order:
                return jsonify({'error': 'Order not found'}), 404
            
            order.cust_id = request.json['customer_id']
            order.emp_id = request.json['emp_id']
            order.status = request.json['status']
            if order.status == 'completed':
                transaction = Invoice.query.filter_by(order_id=id).first()
                transaction.status = 'completed'
                db.session.add(transaction)
            db.session.commit()
            return jsonify({'message': 'Order updated successfully', 'status':200}), 200
        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400