from flask import Blueprint, request, jsonify
from main import db
from models.user import Product, ProductItem
from sqlalchemy.exc import IntegrityError
import os
from dependencies.authentication import token_required_test
from utils.general import object_as_dict
secret_key = os.getenv("SECRET_KEY")


product_blueprint = Blueprint('product', __name__, url_prefix='/product')

@product_blueprint.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            # Extracting details from the request
            name = request.json['name']
            sale_price = request.json['sale_price']
            cost_price = request.json['cost_price']
            description = request.json['description']
            supplier_id = request.json['supplier_id']
            image=None
            if request.json.get('image'):
                image = request.json['image']
            new_product = Product(name=name, sale_price=sale_price, cost_price=cost_price, description=description, image=image)
            db.session.add(new_product)
            db.session.commit()
            new_product_item = ProductItem(product_id=new_product.id, supplier_id=supplier_id)
            db.session.add(new_product_item)
            db.session.commit()
            return jsonify({'message': 'Product created successfully'}), 201

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400
        
        
@product_blueprint.route('/get', methods=['GET'])
def get():
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            products = Product.query.all()
            return jsonify([object_as_dict(product) for product in products]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@product_blueprint.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            product = Product.query.filter_by(id=id).first()
            if not product:
                return jsonify({'error': 'Product not found'}), 404
            return jsonify(object_as_dict(product)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@product_blueprint.route('/update/<int:id>', methods=['PUT'])
def update(id):
    if request.method == 'PUT':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            product = Product.query.filter_by(id=id).first()
            if not product:
                return jsonify({'error': 'Product not found'}), 404
            if request.json.get('name'):
                product.name = request.json['name']
            if request.json.get('sale_price'):
                product.sale_price = request.json['sale_price']
            if request.json.get('cost_price'):
                product.cost_price = request.json['cost_price']
            if request.json.get('description'):
                product.description = request.json['description']
            if request.json.get('image'):
                product.image = request.json['image']
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200
        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@product_blueprint.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    if request.method == 'DELETE':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            product = Product.query.filter_by(id=id).first()
            if not product:
                return jsonify({'error': 'Product not found'}), 404
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500