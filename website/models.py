from . import db #importing the database from __init__.py
from flask_login import UserMixin #used for user authentication
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Customer(db.Model, UserMixin): 
    #setting the column names and values for the customer database
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    passwordHash = db.Column(db.String(150))
    dateJoined = db.Column(db.DateTime(), default=datetime.utcnow)

    #defining the relationships between the tables, lazy=True emits a SELECT statement when loading
    basketItems = db.relationship('Basket', backref = db.backref('customer', lazy=True))
    orders = db.relationship('Order', backref = db.backref('customer', lazy=True)) 

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute') 

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password=password) #securely hashes the password

    def verifyPassword(self, password):
        return check_password_hash(self.passwordHash, password=password) #checks the password against the hashed password
    def __str__(self):
        return '<Customer %r>' % Customer.id  #returns readable values from the database

class Product(db.Model):
    #setting column names and values for the product database
    id = db.Column(db.Integer, primary_key = True)
    productName = db.Column(db.String(100), nullable=False) #nullable = False to ensure as there must be data in these columns
    price = db.Column(db.Float, nullable=False)
    itemAmount = db.Column(db.Integer, nullable=False)
    productPicture = db.Column(db.String(1000), nullable=False)
    dateAdded = db.Column(db.DateTime, default=datetime.utcnow)

    baskets = db.relationship('Basket', backref=db.backref('product', lazy=True))
    orders = db.relationship('Order', backref=db.backref('product', lazy=True))

    def __str__(self):
        return '<Product %r>' % self.productName #returns a readable form of the product

class Basket(db.Model):
    #setting column names and value types of the basket database
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    customerLink = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False) #creates a relationship between this and Customer
    productLink = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) #creates a column to link the table with Product

    def __str__(self):
        return '<Basket %r>' % self.id #returns a readable form of the basket

class Order(db.Model):
    #setting column names and value types for the order database
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)
    paymentID = db.Column(db.String, nullable=False)

    customerLink = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)  #creates a column to link the table with the customer table
    productLink = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    


    def __str__(self):
        return '<Order %r>' % self.id #returns a readable form of the order

