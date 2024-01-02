import datetime
from main import db

class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id', ondelete='CASCADE'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'))
    total = db.Column(db.Integer)
    status = db.Column(db.String(100), default='pending')
class Ledger(db.Model):
    __tablename__ = 'ledger'
    id = db.Column(db.Integer, primary_key=True)
    file_data = db.Column(db.LargeBinary)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)