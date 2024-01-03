from flask import Blueprint, request, jsonify
from main import db
from models.order import Orders, OrderItem
from models.transaction import Invoice
from sqlalchemy.exc import IntegrityError
from dependencies.authentication import token_required_test
from utils.general import object_as_dict

transaction_blueprint = Blueprint('transaction', __name__, url_prefix='/transaction')

@transaction_blueprint.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            items = OrderItem.query.filter_by(order_id=request.json['order_id']).all()
            total=sum([item.quantity * item.unit_price for item in items])
            new_transaction = Invoice(order_id=request.json['order_id'], total=total, user_id=cur_user.id)
            db.session.add(new_transaction)
            db.session.commit()
            return jsonify({'message': 'Transaction created successfully'}), 201

        except IntegrityError as e:
            # Extracting details from the IntegrityError
            error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
            return jsonify({'error': error_info}), 500
        except TypeError as e:
            return jsonify({'error': str(e)}), 400
        
@transaction_blueprint.route('/get_all', methods=['GET'])
def get():
    if request.method == 'GET':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            transactions = Invoice.query.all()
            return jsonify({'transactions':[object_as_dict(transaction) for transaction in transactions], 'status':200}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@transaction_blueprint.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):
    if request.method == 'GET':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            transaction = Invoice.query.filter_by(id=id).first()
            if not transaction:
                return jsonify({'error': 'Transaction not found'}), 404
            return jsonify(object_as_dict(transaction)), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@transaction_blueprint.route('/get', methods=['GET'])
def get_cur_user():
    if request.method == 'GET':
        try:
            cur_user = token_required_test(request.headers.get("Authorization"))
            if not cur_user:
                return jsonify({"error": "Unauthorization Access"}), 400
            transactions = Invoice.query.filter_by(user_id=cur_user.id).all()
            return jsonify([object_as_dict(transaction) for transaction in transactions]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        
# @transaction_blueprint.route('add_ledger', methods=['POST'])
# def add_ledger():
#     if request.method == 'POST':
#         try:
#             cur_user = token_required_test(request.headers.get("Authorization"))
#             if not cur_user:
#                 return jsonify({"error": "Unauthorization Access"}), 400
#             new_ledger = Ledger(cust_id=cur_user.id, file_data=request.json['file_data'])
#             db.session.add(new_ledger)
#             db.session.commit()
#             return jsonify({'message': 'Ledger created successfully'}), 201

#         except IntegrityError as e:
#             # Extracting details from the IntegrityError
#             error_info = e.orig.diag.message_primary if e.orig.diag.message_primary else str(e.orig)
#             return jsonify({'error': error_info}), 500
#         except TypeError as e:
#             return jsonify({'error': str(e)}), 400