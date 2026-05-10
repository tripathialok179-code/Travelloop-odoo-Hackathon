from flask import Blueprint, request, jsonify
import uuid

# Simple in-memory share store (MVP only)
# In production, use DB table with expiration + permissions
shared_links = {}

share_bp = Blueprint('share', __name__, url_prefix='/api/share')


# CREATE SHARE LINK (for trip or any resource)
@share_bp.route('/create', methods=['POST'])
def create_share_link():
    data = request.get_json()

    resource_type = data.get('type')  # trip | activity | expense | packing
    resource_id = data.get('id')

    if not resource_type or not resource_id:
        return jsonify({"message": "type and id are required"}), 400

    share_id = str(uuid.uuid4())

    shared_links[share_id] = {
        "type": resource_type,
        "id": resource_id
    }

    share_url = f"/api/share/{share_id}"

    return jsonify({
        "message": "Share link created",
        "share_id": share_id,
        "share_url": share_url
    }), 201


# ACCESS SHARED DATA
@share_bp.route('/<share_id>', methods=['GET'])
def access_shared(share_id):
    if share_id not in shared_links:
        return jsonify({"message": "Invalid or expired link"}), 404

    return jsonify({
        "message": "Shared link accessed",
        "data": shared_links[share_id]
    }), 200


# DELETE SHARE LINK
@share_bp.route('/<share_id>', methods=['DELETE'])
def delete_share(share_id):
    if share_id in shared_links:
        del shared_links[share_id]

    return jsonify({"message": "Share link removed"}), 200