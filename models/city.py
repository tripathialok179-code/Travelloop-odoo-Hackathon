from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# assuming db is initialized in your app (extensions or __init__.py)
# from app.extensions import db


class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)

    # basic info
    name = db.Column(db.String(120), nullable=False, unique=True)
    state = db.Column(db.String(120), nullable=True)
    country = db.Column(db.String(120), nullable=False)

    # optional description for tourism context
    description = db.Column(db.Text, nullable=True)

    # optional location data
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # media
    image_url = db.Column(db.String(255), nullable=True)

    # timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # relationship (optional, depends on your Activity model setup)
    # activities = db.relationship('Activity', backref='city_ref', lazy=True)

    def __repr__(self):
        return f"<City {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "state": self.state,
            "country": self.country,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
