from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# assuming db is initialized in your app (extensions or __init__.py)
# from app.extensions import db


class PackingItem(db.Model):
    __tablename__ = 'packing_items'

    id = db.Column(db.Integer, primary_key=True)

    # optional links
    trip_id = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)

    # item details
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=True)  # clothes, electronics, essentials, etc.

    quantity = db.Column(db.Integer, default=1)

    # status tracking
    is_packed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(20), default="medium")  # low, medium, high

    # optional notes
    notes = db.Column(db.Text, nullable=True)

    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PackingItem {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "user_id": self.user_id,
            "name": self.name,
            "category": self.category,
            "quantity": self.quantity,
            "is_packed": self.is_packed,
            "priority": self.priority,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }