from main import db
from enum import Enum


class OrderStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    
class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
    ordered_date = db.Column(db.Date)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)