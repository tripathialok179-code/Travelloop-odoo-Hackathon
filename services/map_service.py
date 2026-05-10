import math
from app.models.city import City
from app.models.activity import Activity


class MapService:
    """
    Service layer for map-related logic:
    - distance calculation
    - nearby cities/activities
    - basic geo utilities
    """

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two lat/long points in KM."""
        R = 6371  # Earth radius in km

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)

        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_phi / 2) ** 2
            + math.cos(phi1)
            * math.cos(phi2)
            * math.sin(delta_lambda / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    @staticmethod
    def find_nearby_cities(lat, lon, radius_km=50):
        """Return cities within a given radius."""
        cities = City.query.filter(
            City.latitude.isnot(None),
            City.longitude.isnot(None)
        ).all()

        nearby = []

        for city in cities:
            distance = MapService.haversine_distance(
                lat, lon, city.latitude, city.longitude
            )

            if distance <= radius_km:
                city_data = city.to_dict()
                city_data["distance_km"] = round(distance, 2)
                nearby.append(city_data)

        return sorted(nearby, key=lambda x: x["distance_km"])

    @staticmethod
    def find_nearby_activities(city_id, limit=10):
        """Get activities for a city (basic version)."""
        activities = Activity.query.filter_by(city_id=city_id).limit(limit).all()

        return [a.to_dict() for a in activities]

    @staticmethod
    def suggest_travel_hubs(lat, lon):
        """Suggest top nearby cities as travel hubs."""
        nearby = MapService.find_nearby_cities(lat, lon, radius_km=200)

        return {
            "count": len(nearby),
            "suggestions": nearby[:5]  # top 5
        }
