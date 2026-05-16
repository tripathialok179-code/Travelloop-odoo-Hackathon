from flask import Blueprint, jsonify, request
import requests
from config import Config
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/unsplash/city', methods=['GET'])
def get_city_image():
    city = request.args.get('city', 'India')
    api_key = Config.UNSPLASH_API_KEY
    if not api_key or api_key == 'your_unsplash_api_key_here':
        # Default placeholder if no key
        return jsonify({"url": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800"}), 200
        
    url = f"https://api.unsplash.com/search/photos?query={city}+landscape&client_id={api_key}&per_page=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            return jsonify({"url": data['results'][0]['urls']['regular']}), 200
    return jsonify({"url": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?auto=format&fit=crop&w=800"}), 200

@api_bp.route('/gemini/suggest', methods=['POST'])
def gemini_suggest():
    data = request.json
    destination = data.get('destination', 'India')
    days = data.get('days', 3)
    start_point = data.get('start_point', 'Unknown')
    transport_mode = data.get('transport_mode', 'Flight')
    vehicle_model = data.get('vehicle_model', '')
    num_people = data.get('num_people', 1)
    
    api_key = Config.GEMINI_API_KEY
    if not api_key or api_key == 'your_gemini_api_key_here':
        return jsonify({"error": "Gemini API key not configured. Please add it to .env"}), 400
        
    prompt = f"Provide a comprehensive {days}-day travel itinerary from {start_point} to {destination} for {num_people} people traveling by {transport_mode} {('using vehicle '+vehicle_model) if vehicle_model else ''}. You MUST return ONLY valid JSON with exactly three keys: 'itinerary' (array of strings, detailing day-by-day activities and the journey), 'total_budget_inr' (integer, total estimated cost for ALL {num_people} people), and 'cost_breakdown' (object containing exactly these keys: 'transportation', 'accommodation', 'food', 'activities' with string values estimating cost in INR)."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = text.replace('```json', '').replace('```', '').strip()
            return jsonify(json.loads(text)), 200
        else:
            return jsonify({"error": "Failed to fetch from Gemini", "details": response.text}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/gemini/manage_summary', methods=['POST'])
def gemini_manage_summary():
    data = request.json
    trip_id = data.get('trip_id')
    from models import db
    from models.trip import Trip
    trip = Trip.query.get(trip_id)
    if not trip: return jsonify({"error": "No trip"}), 404
    destination = trip.destination
    api_key = Config.GEMINI_API_KEY
    if not api_key or api_key == 'your_gemini_api_key_here': return jsonify({"error": "No key"}), 400
    
    prompt = f"Provide a brief, engaging travel summary for {destination}. Return ONLY valid JSON with exactly these keys: 'summary' (string, engaging paragraph), 'best_time_to_visit' (string), and 'transportation_options' (array of strings, detailing how to get around)."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = text.replace('```json', '').replace('```', '').strip()
            trip.ai_summary = text
            db.session.commit()
            return jsonify(json.loads(text)), 200
        return jsonify({"error": "Failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/gemini/manage_budget', methods=['POST'])
def gemini_manage_budget():
    data = request.json
    trip_id = data.get('trip_id')
    from models import db
    from models.trip import Trip
    trip = Trip.query.get(trip_id)
    if not trip: return jsonify({"error": "No trip"}), 404
    destination = trip.destination
    api_key = Config.GEMINI_API_KEY
    if not api_key or api_key == 'your_gemini_api_key_here': return jsonify({"error": "No key"}), 400
    
    prompt = f"Provide 3 distinct budget tiers for traveling in {destination} for {trip.days} days and {trip.num_people} people. Return ONLY valid JSON with exactly this structure: 'budget_tiers' (array of exactly 3 objects for 'backpacking', 'standard', 'luxury'. Each object MUST have exactly these keys: 'tier_name' (string), 'total_cost' (string INR), 'breakdown' (object containing keys 'food', 'transport', 'accommodation', 'activities' with string values in INR), and 'specific_tips' (array of strings))."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = text.replace('```json', '').replace('```', '').strip()
            return jsonify(json.loads(text)), 200
        return jsonify({"error": "Failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/gemini/route_logistics', methods=['POST'])
def gemini_route_logistics():
    data = request.json
    trip_id = data.get('trip_id')
    from models import db
    from models.trip import Trip
    trip = Trip.query.get(trip_id)
    if not trip: return jsonify({"error": "No trip"}), 404
    start = trip.start_point
    dest = trip.destination
    mode = trip.transport_mode
    vehicle = trip.vehicle_model
    api_key = Config.GEMINI_API_KEY
    if not api_key: return jsonify({"error": "No key"}), 400
    
    prompt = f"Provide a realistic travel summary from {start} to {dest} using {mode} {('('+vehicle+')') if vehicle else ''}. Return ONLY valid JSON with exactly these keys: 'logistics_summary' (string paragraph discussing tolls, petrol costs, frequent trains/buses/flights depending on mode), and 'insights' (array of strings, bullet points of key travel details)."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = text.replace('```json', '').replace('```', '').strip()
            trip.ai_logistics = text
            db.session.commit()
            return jsonify(json.loads(text)), 200
        return jsonify({"error": "Failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/trip/save_budget', methods=['POST'])
def save_trip_budget():
    data = request.json
    trip_id = data.get('trip_id')
    selected_tier = data.get('selected_tier')
    from models import db
    from models.trip import Trip
    trip = Trip.query.get(trip_id)
    if not trip: return jsonify({"error": "No trip"}), 404
    import json
    trip.ai_budget = json.dumps(selected_tier)
    cost_str = str(selected_tier.get('total_cost', '0')).replace(',', '').replace('₹', '').replace(' ', '').replace('INR', '')
    try:
        trip.budget = float(cost_str)
    except:
        trip.budget = 0.0
    db.session.commit()
    return jsonify({"status": "success"}), 200

@api_bp.route('/gemini/packing', methods=['POST'])
def gemini_packing():
    data = request.json
    trip_id = data.get('trip_id')
    from models import db
    from models.trip import Trip
    trip = Trip.query.get(trip_id)
    if not trip: return jsonify({"error": "No trip"}), 404
    destination = trip.destination
    api_key = Config.GEMINI_API_KEY
    if not api_key: return jsonify({"error": "No key"}), 400
    
    prompt = f"Provide a practical travel packing list for {destination} considering the general climate. Return ONLY valid JSON with exactly one key: 'packing_items' (array of strings)."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            text = result['candidates'][0]['content']['parts'][0]['text']
            text = text.replace('```json', '').replace('```', '').strip()
            trip.ai_packing = text
            db.session.commit()
            return jsonify(json.loads(text)), 200
        return jsonify({"error": "Failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/trip/save_packing', methods=['POST'])
def save_trip_packing():
    data = request.json
    trip_id = data.get('trip_id')
    items = data.get('items', [])
    from models import db
    from models.trip import Trip
    trip = Trip.query.get(trip_id)
    if not trip: return jsonify({"error": "No trip"}), 404
    import json
    trip.ai_packing = json.dumps({"packing_items": items})
    db.session.commit()
    return jsonify({"status": "success"}), 200
