from flask import Blueprint, request, jsonify
from main import db
from models.product import Images, Product, ProductItem
from sqlalchemy.exc import IntegrityError
from dependencies.authentication import token_required_test
from utils.general import object_as_dict


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
            quantity = request.json['quantity']
            new_product = Product(name=name, sale_price=sale_price, cost_price=cost_price, description=description, total_quantity=quantity)
            db.session.add(new_product)
            db.session.commit()
            if request.json.get('images'):
                for image in request.json['images']:
                    new_image = Images(product_id=new_product.id, image=image)
                    db.session.add(new_image)
            new_product_item = ProductItem(product_id=new_product.id, supplier_id=supplier_id, quantity=quantity)
            db.session.add(new_product_item)
            db.session.commit()
            if sale_price < cost_price:
                return jsonify({'message': 'Warning: added product with lower sale price', "status": 200})
            return jsonify({'message': 'Product created successfully', 'status': 201}), 201

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400
        
@product_blueprint.route('/get_all', methods=['GET'])
def get_all():
    if request.method == 'GET':
        try:
            if not request.headers.get("Authorization") or not token_required_test(request.headers.get("Authorization")):
                return jsonify({"error": "Unauthorization Access"}), 400
            products = Product.query.all()
            products_list = []
            for product in products:
                obj = object_as_dict(product)
                obj["images"] = [image.image for image in Images.query.filter_by(product_id=product.id).all()]
                products_list.append(obj)
            return jsonify({"products":products_list, "status": 200}), 200
        except Exception as e:
            raise e
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
            return jsonify({'message': 'Product updated successfully', 'status':200 }), 200
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
            product_items = ProductItem.query.filter_by(product_id=id).all()
            for product_item in product_items:
                db.session.delete(product_item)
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully', 'status': 200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
