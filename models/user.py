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
