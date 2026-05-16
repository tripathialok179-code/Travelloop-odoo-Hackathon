from models import db
from datetime import datetime

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    destination = db.Column(db.String(150))
    start_point = db.Column(db.String(150))
    transport_mode = db.Column(db.String(50))
    vehicle_model = db.Column(db.String(150))
    num_people = db.Column(db.Integer, default=1)
    days = db.Column(db.Integer, default=7)
    description = db.Column(db.Text)
    ai_summary = db.Column(db.Text)
    ai_logistics = db.Column(db.Text)
    ai_budget = db.Column(db.Text)
    ai_packing = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float, default=0.0)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
