from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# assuming db is initialized in your app (extensions or __init__.py)
# from app.extensions import db


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)

    # optional link to trip (if your app has trip module)
    trip_id = db.Column(db.Integer, nullable=True)

    # optional user who added expense
    user_id = db.Column(db.Integer, nullable=True)

    # basic expense info
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # financial data
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="INR")

    # category (food, travel, stay, shopping, misc)
    category = db.Column(db.String(50), nullable=False)

    # date of expense
    expense_date = db.Column(db.DateTime, default=datetime.utcnow)

    # split info (simple approach for hackathon MVP)
    is_shared = db.Column(db.Boolean, default=False)
    split_count = db.Column(db.Integer, default=1)

    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Expense {self.title} - {self.amount}>"

    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "amount": self.amount,
            "currency": self.currency,
            "category": self.category,
            "expense_date": self.expense_date.isoformat() if self.expense_date else None,
            "is_shared": self.is_shared,
            "split_count": self.split_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }