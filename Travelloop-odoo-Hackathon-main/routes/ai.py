from flask import Blueprint
from flask import jsonify
from flask import request

from services.ai_services import (
    test_ai,
    generate_trip_plan
)

ai_bp = Blueprint(
    "ai",
    __name__,
    url_prefix="/ai"
)


# --------------------------------
# TEST AI ROUTE
# --------------------------------
@ai_bp.route("/test")
def ai_test():

    result = test_ai()

    return jsonify({
        "result": result
    })


# --------------------------------
# GENERATE TRIP ROUTE
# --------------------------------
@ai_bp.route(
    "/generate-trip",
    methods=["POST"]
)
def generate_trip():

    data = request.json

    result = generate_trip_plan(data)

    return jsonify({
        "trip": result
    })
