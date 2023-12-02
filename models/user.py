from main import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    contact = db.Column(db.Numeric)
    role = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': role
    }  # Indicates the type of the users
class Admin(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'admin'}  # Indicates the type of the users

class Customer(User):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'customer'}  # Indicates the type of the users

class Supplier(User):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'supplier'}  # Indicates the type of the users
    
class Employee(User):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'employee'}  # Indicates the type of the users

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sale_price = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Integer)
    image = db.Column(db.LargeBinary)
    description = db.Column(db.String)

class ProductItem(db.Model):
    __tablename__ = 'product_item'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), primary_key=True)

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    ordered_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)

class Invoice(db.Model):
    __tablename__ = 'invoice'
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    total_payment = db.Column(db.Integer)
    remaining_payment = db.Column(db.Integer)

class Ledger(db.Model):
    __tablename__ = 'ledger'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    file_data = db.Column(db.LargeBinary)
