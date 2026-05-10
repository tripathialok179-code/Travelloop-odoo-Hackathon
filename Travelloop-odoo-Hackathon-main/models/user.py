from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50)) # cite: 31
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False) # cite: 31
    phone_number = db.Column(db.String(20))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    
    # Relationship: One user can have many trips
    trips = db.relationship('Trip', backref='owner', lazy=True)