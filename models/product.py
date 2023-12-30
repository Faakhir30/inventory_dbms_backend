from main import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sale_price = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Integer)
    image = db.Column(db.String, default='default.jpg')
    description = db.Column(db.String)
    total_quantity = db.Column(db.Integer, nullable=False)

class ProductItem(db.Model):
    __tablename__ = 'product_item'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    quantity = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)