from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# assuming db is initialized in your app/__init__.py
# from your project import db

# If you are using application factory pattern, you will import db from extensions
# from app.extensions import db


class Activity(db.Model):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)

    # basic info
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # type of activity (hotel, sightseeing, food, adventure etc.)
    category = db.Column(db.String(50), nullable=False)

    # location info
    location = db.Column(db.String(150), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    # pricing
    price = db.Column(db.Float, default=0.0)

    # rating system
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)

    # media
    image_url = db.Column(db.String(255), nullable=True)

    # time tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Activity {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "location": self.location,
            "city": self.city,
            "country": self.country,
            "price": self.price,
            "rating": self.rating,
            "review_count": self.review_count,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
