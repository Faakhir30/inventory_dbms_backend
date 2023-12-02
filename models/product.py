from main import db

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
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), primary_key=True)
