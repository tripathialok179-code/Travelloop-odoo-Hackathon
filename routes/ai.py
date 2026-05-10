from flask import Blueprint, jsonify
from services.ai_services import test_ai

ai_bp = Blueprint(
    "ai",
    __name__,
    url_prefix="/ai"
)

@ai_bp.route("/test")
def ai_test():

    result = test_ai()

    return jsonify({
        "result": result
    })