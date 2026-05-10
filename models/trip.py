from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# assuming db is initialized in your app (extensions or __init__.py)
# from app.extensions import db


class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)

    # basic info
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # who created / owns the trip
    user_id = db.Column(db.Integer, nullable=False)

    # destination (can be linked to City model optionally)
    city_id = db.Column(db.Integer, nullable=True)
    destination = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(100), nullable=True)

    # trip dates
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    # budget tracking
    budget = db.Column(db.Float, default=0.0)
    total_spent = db.Column(db.Float, default=0.0)

    # status
    status = db.Column(db.String(50), default="planned")  # planned, ongoing, completed

    # optional metadata
    travelers_count = db.Column(db.Integer, default=1)

    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationships (optional, enable when models are fully wired)
    # activities = db.relationship('Activity', backref='trip', lazy=True)
    # expenses = db.relationship('Expense', backref='trip', lazy=True)
    # packing_items = db.relationship('PackingItem', backref='trip', lazy=True)

    def __repr__(self):
        return f"<Trip {self.title} - {self.destination}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
            "city_id": self.city_id,
            "destination": self.destination,
            "country": self.country,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "budget": self.budget,
            "total_spent": self.total_spent,
            "status": self.status,
            "travelers_count": self.travelers_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }