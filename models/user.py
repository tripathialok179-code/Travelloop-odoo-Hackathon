from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# assuming db is initialized in your app (extensions or __init__.py)
# from app.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    # basic info
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)

    # authentication
    password_hash = db.Column(db.String(255), nullable=False)

    # optional profile info
    profile_pic = db.Column(db.String(255), nullable=True)

    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships (enable when wiring full system)
    # trips = db.relationship('Trip', backref='user', lazy=True)
    # expenses = db.relationship('Expense', backref='user', lazy=True)
    # packing_items = db.relationship('PackingItem', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

    # password helpers
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "profile_pic": self.profile_pic,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }