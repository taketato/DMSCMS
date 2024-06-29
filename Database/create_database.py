from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.dialects.postgresql import ARRAY

app = Flask(__name__)
# update
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_for_9900.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tt:123456@localhost/database_for_9900'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(500), nullable=True)
    sc_address = db.Column(db.String(100), nullable=True)
    # add relationship with Product and Production
    Products = db.relationship('Product', backref='ProductOwner', lazy=True)
    Productions = db.relationship('Inventory', backref='InventoryOwner', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100), nullable=False)
    # add foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Items_Product = db.relationship('Items', backref='Items2Product', lazy=True)
    Inventory_Product = db.relationship('Inventory', backref='Inventory2Product', lazy=True)


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100))
    # type = db.Column(db.String(100), nullable=False)
    # update name and add productId
    pid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    InventoryQuantity = db.Column(db.Integer)
    DemandQuantity = db.Column(db.Integer, nullable=True)
    # date_of_production = db.Column(db.String(100), nullable=False)
    # add foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    # update
    name = db.Column(db.String(100))
    sc_address = db.Column(db.String(100), nullable=True)
    # update
    SourceAddress = db.Column(db.String(100), nullable=True)
    Destination = db.Column(db.String(100), nullable=True)
    SendTime = db.Column(db.String(100), nullable=False)
    ReceiveTime = db.Column(db.String(100), nullable=True)
    # update
    # An array column to store productIds and quantities
    # ProductIds = db.Column(ARRAY(db.String()))
    # Quantities = db.Column(ARRAY(db.String()))
    ProductId = db.Column(db.String(500), nullable=False)
    Quantities = db.Column(db.String(500), nullable=False)
    # product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

# update
class Items (db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    #pid = db.Column(db.Integer, db.ForeignKey('product.id'))
    ProduceTime = db.Column(db.String(100), nullable=False)
    # update
    # DeliveryIds = db.Column(ARRAY(db.String()))
    DeliveryIds = db.Column(db.String(500), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class contract_ABI(db.Model):
    contract_name = db.Column(db.String, primary_key=True, unique=True)
    SC_ABI = db.Column(db.String(200), nullable=False)


@app.route('/init_db')
def init_db():
    db.drop_all()  # Be cautious with this line; it will drop all existing tables in the database
    db.create_all()
    return "Database initialized."


if __name__ == '__main__':
    app.run(debug=True)
