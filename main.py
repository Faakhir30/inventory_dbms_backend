from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# from psycopg2 import connect


app = Flask(__name__)
CORS(app , origins=["http://localhost:3000", "*"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/inventory_dbms'
db = SQLAlchemy()
db.init_app(app)


from endpoints.auth import auth_blueprint
from endpoints.product import product_blueprint
from endpoints.order import order_blueprint


app.register_blueprint(order_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(product_blueprint)


with app.app_context():
    db.create_all()    
    
    
@app.route('/', methods=['GET', 'POST'])
def home(request):
    if request.method == 'GET':
        return jsonify({'message': 'Hello, World!'})
    return 'kausydf'

if __name__ == '__main__':
    app.run(debug=True, port=5000)