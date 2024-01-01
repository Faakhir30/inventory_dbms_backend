from main import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sale_price = db.Column(db.Integer, nullable=False)
    cost_price = db.Column(db.Integer)
    description = db.Column(db.String)
    total_quantity = db.Column(db.Integer, nullable=False)

class ProductItem(db.Model):
    __tablename__ = 'product_item'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    quantity = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))
    image = db.Column(db.String, default='default.jpg')