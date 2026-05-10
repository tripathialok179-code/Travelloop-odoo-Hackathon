from flask import Blueprint, request, jsonify
from models.trip import db, Trip, Stop

trip_bp = Blueprint('trip', __name__)

@trip_bp.route('/add-stop', methods=['POST'])
def add_stop():
    data = request.json
    new_stop = Stop(
        trip_id=data['trip_id'],
        city_name=data['city_name'],
        arrival_date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_stop)
    db.session.commit()
    return jsonify({"message": "Stop added successfully"}), 201