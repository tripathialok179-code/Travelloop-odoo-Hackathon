from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.city import City

cities_bp = Blueprint('cities', __name__, url_prefix='/api/cities')


# GET all cities
@cities_bp.route('/', methods=['GET'])
def get_cities():
    cities = City.query.all()
    return jsonify([c.to_dict() for c in cities]), 200


# GET single city
@cities_bp.route('/<int:city_id>', methods=['GET'])
def get_city(city_id):
    city = City.query.get_or_404(city_id)
    return jsonify(city.to_dict()), 200


# CREATE city
@cities_bp.route('/', methods=['POST'])
def create_city():
    data = request.get_json()

    name = data.get('name')
    country = data.get('country')

    if not name or not country:
        return jsonify({"message": "name and country are required"}), 400

    existing_city = City.query.filter_by(name=name).first()
    if existing_city:
        return jsonify({"message": "City already exists"}), 409

    city = City(
        name=name,
        state=data.get('state'),
        country=country,
        description=data.get('description'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        image_url=data.get('image_url')
    )

    db.session.add(city)
    db.session.commit()

    return jsonify(city.to_dict()), 201


# UPDATE city
@cities_bp.route('/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    city = City.query.get_or_404(city_id)
    data = request.get_json()

    city.name = data.get('name', city.name)
    city.state = data.get('state', city.state)
    city.country = data.get('country', city.country)
    city.description = data.get('description', city.description)
    city.latitude = data.get('latitude', city.latitude)
    city.longitude = data.get('longitude', city.longitude)
    city.image_url = data.get('image_url', city.image_url)

    db.session.commit()

    return jsonify(city.to_dict()), 200


# DELETE city
@cities_bp.route('/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = City.query.get_or_404(city_id)

    db.session.delete(city)
    db.session.commit()

    return jsonify({"message": "City deleted successfully"}), 200