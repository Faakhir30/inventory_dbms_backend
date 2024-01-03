from flask import Blueprint, request, jsonify
from main import db
from models.product import Product, ProductItem
from sqlalchemy.exc import IntegrityError
from dependencies.authentication import token_required_test
from utils.general import object_as_dict


product_item_blueprint = Blueprint('product_item', __name__, url_prefix='/product_item')

@product_item_blueprint.route('/get_all', methods=['GET'])
def get_all():
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            product_items = ProductItem.query.all()
            return jsonify({"product_items":[object_as_dict(product_item) for product_item in product_items], "status": 200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@product_item_blueprint.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            product_item = ProductItem.query.filter_by(product_id=id).first()
            if not product_item:
                return jsonify({'error': 'No product_item found!'}), 404
            return jsonify({"product_item":object_as_dict(product_item), "status": 200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@product_item_blueprint.route('/update/<int:id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            product_item = ProductItem.query.filter_by(product_id=id).first()
            if not product_item:
                return jsonify({'error': 'No product_item found!'}), 404
            product = Product.query.filter_by(id=product_item.product_id).first()
            product.total_quantity -= product_item.quantity
            product.total_quantity += request.json['quantity']
            product_item.quantity = request.json['quantity']
            db.session.commit()
            return jsonify({'message': 'Product_item updated successfully', 'status':200}), 200
        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@product_item_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            product_item = ProductItem.query.filter_by(id=id).first()
            if not product_item:
                return jsonify({'error': 'No product_item found!'}), 404
            product = Product.query.filter_by(id=product_item.product_id).first()
            product.total_quantity -= product_item.quantity
            db.session.delete(product_item)
            db.session.commit()
            return jsonify({'message': 'Product_item deleted successfully', 'status':200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@product_item_blueprint.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            
            product_item = ProductItem(
                product_id=request.json['product_id'],
                supplier_id=request.json['supplier_id'],
                quantity=int(request.json['quantity'])
            )
            product = Product.query.filter_by(id=product_item.product_id).first()
            product.total_quantity += product_item.quantity
            db.session.add(product)
            db.session.add(product_item)
            db.session.commit()
            return jsonify({'message': 'Product_item added successfully', 'status':200}), 200
        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@product_item_blueprint.route('/get_by_supplier/<int:id>', methods=['GET'])
def get_by_supplier(id):
    if request.method == 'GET':
        try:
            product_items = ProductItem.query.filter_by(supplier_id=id).all()
            if not product_items:
                return jsonify({'error': 'No product_item found!'}), 404
            return jsonify({"product_items":[object_as_dict(product_item) for product_item in product_items], "status": 200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@product_item_blueprint.route('/get_by_product/<int:id>', methods=['GET'])
def get_by_product(id):
    if request.method == 'GET':
        try:
            product_items = ProductItem.query.filter_by(product_id=id).all()
            if not product_items:
                return jsonify({'error': 'No product_item found!'}), 404
            return jsonify({"product_items":[object_as_dict(product_item) for product_item in product_items], "status": 200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
