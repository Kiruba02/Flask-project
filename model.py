import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)

# DB Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admini@localhost:3306/Project_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    cash_balance = db.Column(db.Integer, nullable=False)


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    qty = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Integer, nullable=False)


class Purchase(db.Model):
    purchase_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    item = db.relationship("Item", backref=backref("purchase_item", uselist=False))
    qty = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Sales(db.Model):
    sales_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    item = db.relationship("Item", backref=backref("sale_item", uselist=False))
    qty = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
