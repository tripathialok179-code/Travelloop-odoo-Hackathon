import os

files = {
    'templates/itinerary_view.html': '''{% extends 'trip_layout.html' %}
{% block trip_content %}
<h2>Comprehensive AI Breakdown</h2>
<p style="margin-bottom: 2rem;">Review your trip specifics or dynamically generate AI insights for {{ trip.destination }}.</p>

<!-- NEW AI INSIGHTS CARD -->
<div class="card" style="margin-bottom: 2rem; border-color: var(--accent);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color:var(--accent)">✨</span> Destination Insights & Transport Guide
        </h3>
    </div>
    <div id="manage-summary-result" style="color: var(--text-main);">
        {% if ai_summary %}
            <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">{{ ai_summary.summary }}</p>
            <div style="background: rgba(0,0,0,0.05); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <h4 style="color: var(--accent); margin-bottom: 0.5rem;">✨ Best Time To Visit</h4>
                <p>{{ ai_summary.best_time_to_visit }}</p>
            </div>
            <h4>Transportation Options</h4>
            <ul style="margin-top: 0.5rem; padding-left: 1.5rem; color: var(--text-muted);">
            {% for opt in ai_summary.transportation_options %}
                <li style="margin-bottom: 0.5rem;">{{ opt }}</li>
            {% endfor %}
            </ul>
        {% else %}
            <p style="color: var(--accent); font-weight: 500;">✨ Gemini is generating your trip summary automatically...</p>
        {% endif %}
    </div>
</div>
{% endblock %}
{% block trip_scripts %}
{% if not ai_summary %}
<script>
    document.addEventListener("DOMContentLoaded", function() {
        generateTripSummary({{ trip.id }}, 'manage-summary-result');
    });
</script>
{% endif %}
{% endblock %}''',
    
    'templates/itinerary_builder.html': '''{% extends 'trip_layout.html' %}
{% block trip_content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
    <h2>AI Recommended Route Map & Logistics</h2>
</div>

<div class="card" style="margin-bottom: 2rem; border-color: var(--accent);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color:var(--accent)">✨</span> Real-World Travel Routes & Logistics
        </h3>
    </div>
    <div id="route-logistics-result" style="color: var(--text-main);">
        {% if ai_logistics %}
        <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">{{ ai_logistics.logistics_summary }}</p>
        <h4>Detailed Insights</h4>
        <ul style="margin-top: 0.5rem; padding-left: 1.5rem; color: var(--text-muted);">
            {% for opt in ai_logistics.insights %}
            <li style="margin-bottom: 0.5rem;">{{ opt }}</li>
            {% endfor %}
        </ul>
        {% else %}
        <p style="color: var(--accent); font-weight: 500;">✨ Gemini is finding the best trains, buses, flights, and road routes...</p>
        {% endif %}
    </div>
</div>

<div class="grid" style="grid-template-columns: 1fr;">
    <div class="card" style="padding: 0; overflow: hidden; width: 100%;">
        <div id="map" style="width: 100%; height: 100%; min-height: 500px; z-index: 1;"></div>
    </div>
</div>
{% endblock %}
{% block trip_scripts %}
<link rel="stylesheet" href="https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.css" />
<script src="https://unpkg.com/leaflet-routing-machine@latest/dist/leaflet-routing-machine.js"></script>
<script>
    window.map = L.map('map').setView([20.5937, 78.9629], 4);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(window.map);

    async function routeTrip(start, dest) {
        if (!start || !dest || start === 'None' || dest === 'None') return;
        try {
            const res1 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(start)}`);
            const d1 = await res1.json();
            const res2 = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(dest)}`);
            const d2 = await res2.json();

            if (d1.length > 0 && d2.length > 0) {
                L.Routing.control({
                    waypoints: [
                        L.latLng(d1[0].lat, d1[0].lon),
                        L.latLng(d2[0].lat, d2[0].lon)
                    ],
                    lineOptions: { styles: [{ color: '#4F46E5', weight: 4 }] },
                    show: false,
                    addWaypoints: false,
                    routeWhileDragging: false,
                    fitSelectedRoutes: true
                }).addTo(window.map);
            }
        } catch (e) { console.error("Map routing error", e); }
    }

    routeTrip('{{ trip.start_point }}', '{{ trip.destination }}');

    {% if not ai_logistics %}
    document.addEventListener("DOMContentLoaded", function () {
        generateTravelLogistics({{ trip.id }}, 'route-logistics-result');
    });
    {% endif %}
</script>
{% endblock %}''',
    
    'templates/budget.html': '''{% extends 'trip_layout.html' %}
{% block trip_content %}
<h2>Detailed Cost Breakdown</h2>
<p style="margin-bottom: 2rem;">Every single transportation, lodging, food, and activity cost calculated dynamically for your group of {{ trip.num_people }}.</p>

<div class="card" style="margin-bottom: 2rem; border-color: var(--accent);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color:var(--accent)">✨</span> AI Daily Budget Estimator
        </h3>
        <div style="display: flex; gap: 0.5rem;">
            <button class="btn btn-secondary" style="border-color: var(--accent); color: var(--accent);" onclick="document.getElementById('manage-budget-result').innerHTML = '<p style=\'color: var(--accent); font-weight: 500;\'>✨ Gemini is recalculating...</p>'; generateTripBudget({{ trip.id }}, 'manage-budget-result')">Regenerate Budget Tiers</button>
        </div>
    </div>
    <div id="manage-budget-result" style="color: var(--text-main);">
        {% if ai_budget %}
            <div class="card" style="border: 2px solid var(--accent); padding: 1.5rem; background: rgba(79, 70, 229, 0.03);">
                <p style="text-transform: uppercase; font-size: 0.8rem; font-weight: bold; color: var(--text-muted);">Current Active Plan: {{ ai_budget.tier_name }}</p>
                <h3 style="color: var(--accent); font-size: 2.5rem; margin: 0.5rem 0;">₹ {{ ai_budget.total_cost }}</h3>
                <p style="font-size: 0.9rem; margin-bottom: 2rem; opacity: 0.8;">Comprehensive estimate for {{ trip.days }} days and {{ trip.num_people }} traveler(s)</p>
                
                <div class="grid grid-4" style="gap: 1rem; margin-bottom: 2rem;">
                    <div style="background: var(--bg-color); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">🍔 Food</p>
                        <p style="font-weight: 600;">₹ {{ ai_budget.breakdown.food }}</p>
                    </div>
                    <div style="background: var(--bg-color); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">🚕 Transport</p>
                        <p style="font-weight: 600;">₹ {{ ai_budget.breakdown.transport }}</p>
                    </div>
                    <div style="background: var(--bg-color); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">🏨 Lodging</p>
                        <p style="font-weight: 600;">₹ {{ ai_budget.breakdown.accommodation }}</p>
                    </div>
                    <div style="background: var(--bg-color); padding: 1rem; border-radius: 8px; border: 1px solid var(--border);">
                        <p style="font-size: 0.8rem; color: var(--text-muted);">🎟 Activities</p>
                        <p style="font-weight: 600;">₹ {{ ai_budget.breakdown.activities }}</p>
                    </div>
                </div>

                <h4 style="margin-bottom: 1rem;">💡 Tier-Specific Travel Tips</h4>
                <ul style="padding-left: 1.5rem; color: var(--text-muted);">
                {% for tip in ai_budget.specific_tips %}
                    <li style="margin-bottom: 0.5rem;">{{ tip }}</li>
                {% endfor %}
                </ul>
            </div>
        {% else %}
            <p style="color: var(--accent); font-weight: 500;">✨ Gemini is calculating your comprehensive budget options...</p>
        {% endif %}
    </div>
</div>
{% endblock %}
{% block trip_scripts %}
{% if not ai_budget %}
<script>
    document.addEventListener("DOMContentLoaded", function() {
        generateTripBudget({{ trip.id }}, 'manage-budget-result');
    });
</script>
{% endif %}
{% endblock %}''',

    'templates/packing.html': '''{% extends 'trip_layout.html' %}
{% block trip_content %}
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
    <h2>AI Packing Assistant</h2>
</div>

<div class="card" style="margin-bottom: 2rem; border-color: var(--accent);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color:var(--accent)">✨</span> Destination Climate & Essentials Checklist
        </h3>
    </div>
    <div id="manage-packing-result" style="color: var(--text-main);">
        {% if ai_packing %}
        <p style="color: var(--accent); font-weight: 500;">Your smart packing list. Click ❌ to remove items or manually
            add new ones at the bottom.</p>
        {% else %}
        <p style="color: var(--accent); font-weight: 500;">✨ Gemini is analyzing the climate and compiling your
            essentials...</p>
        {% endif %}
    </div>
</div>

{% endblock %}
{% block trip_scripts %}
<script>
    window.currentTripId = {{ trip.id }};
    {% if ai_packing %}
    // Load persisted list
    window.currentPackingList = {{ ai_packing.packing_items | tojson }};
    renderPackingList('manage-packing-result');
    {% else %}
    document.addEventListener("DOMContentLoaded", function () {
        generatePackingList({{ trip.id }}, 'manage-packing-result');
        });
    {% endif %}
</script>
{% endblock %}''',

    'templates/trip_layout.html': '''{% extends 'layout.html' %}
{% block content %}
<div id="trip-header" class="hero-header">
    <div>
        <h1>{{ trip.title }}</h1>
        <p>{{ trip.start_date.strftime('%b %d') if trip.start_date else 'AI Generated Plan' }}</p>
    </div>
</div>
<div class="sub-nav">
    <a href="{{ url_for('views.itinerary_view', trip_id=trip.id) }}">AI Overview</a>
    <a href="{{ url_for('views.itinerary_builder', trip_id=trip.id) }}">Map & Route</a>
    <a href="{{ url_for('views.budget', trip_id=trip.id) }}">Cost Breakdown</a>
    <a href="{{ url_for('views.packing', trip_id=trip.id) }}">Packing</a>
    <a href="{{ url_for('views.shared_trip', trip_id=trip.id) }}">Share</a>
</div>
{% block trip_content %}{% endblock %}
{% endblock %}
{% block scripts %}
<script>
    fetchCityImage('{{ trip.destination or trip.title }}', 'trip-header');
</script>
{% block trip_scripts %}{% endblock %}
{% endblock %}''',

    'templates/layout.html': '''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travelloop | India</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <!-- Leaflet CSS for Maps -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script>
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.documentElement.setAttribute('data-theme', savedTheme);
    </script>
</head>
<body>
    <nav class="navbar">
        <div class="brand">
            <span style="font-size: 1.5rem;">🌎</span>
            Travelloop
        </div>
        <ul class="nav-links">
            {% if g.user %}
                <li><a href="{{ url_for('views.dashboard') }}">Dashboard</a></li>
                <li><a href="{{ url_for('views.my_trips') }}">My Trips</a></li>
                <li><a href="{{ url_for('views.city_search') }}">Explore India</a></li>
                <li><a href="{{ url_for('views.profile') }}">Profile</a></li>
            {% endif %}
            <li>
                <button onclick="toggleTheme()" class="theme-toggle" id="theme-icon">🌙</button>
            </li>
        </ul>
        <div>
            {% if g.user %}
                <a href="{{ url_for('views.create_trip') }}" class="btn btn-primary">+ Plan Trip</a>
                <a href="{{ url_for('auth.logout') }}" class="btn btn-secondary" style="margin-left: 0.5rem;">Logout</a>
            {% else %}
                <a href="{{ url_for('views.login') }}" class="btn btn-primary">Login / Sign Up</a>
            {% endif %}
        </div>
    </nav>
    <main class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="flash-message {% if category == 'success' %}flash-success{% endif %}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </main>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>''',

    'templates/create_trip.html': '''{% extends 'layout.html' %}
{% block content %}
<div style="max-width: 600px; margin: 0 auto; padding-top: 2rem;">
    <h1 style="margin-bottom: 0.5rem; text-align: center;">Plan Your Journey</h1>
    <p style="margin-bottom: 2rem; text-align: center;">Enter your trip details below to build your itinerary.</p>
    
    <div class="card">
        <div id="dynamic-dest-img" style="height: 150px; background: var(--card-border); background-size: cover; background-position: center; border-radius: 12px; margin-bottom: 1.5rem; transition: background 0.5s ease;"></div>
        <form action="{{ url_for('views.create_trip') }}" method="POST">
            <div class="form-group">
                <label class="form-label">Trip Title</label>
                <input type="text" name="title" class="form-control" placeholder="e.g., Summer Escape" required>
            </div>
            <div class="grid grid-2">
                <div class="form-group">
                    <label class="form-label">Start Point</label>
                    <input type="text" name="start_point" id="ai-start" class="form-control" placeholder="e.g., Delhi" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Destination</label>
                    <input type="text" id="ai-destination" name="destination" class="form-control" placeholder="e.g., Rajasthan" value="{{ request.args.get('destination', '') }}" onblur="fetchCityImage(this.value, 'dynamic-dest-img')" required>
                </div>
            </div>
            <div class="grid grid-2">
                <div class="form-group">
                    <label class="form-label">Transport Mode</label>
                    <select name="transport_mode" id="ai-transport" class="form-control" onchange="document.getElementById('vehicle-group').style.display = this.value === 'Road' ? 'block' : 'none';">
                        <option value="Flight">Flight</option>
                        <option value="Train">Train</option>
                        <option value="Bus">Bus</option>
                        <option value="Road">By Road (Car/Bike)</option>
                    </select>
                </div>
                <div class="form-group" id="vehicle-group" style="display: none;">
                    <label class="form-label">Vehicle Model</label>
                    <input type="text" name="vehicle_model" id="ai-vehicle" class="form-control" placeholder="e.g., Innova">
                </div>
            </div>
            <div class="grid grid-2">
                <div class="form-group">
                    <label class="form-label">No. of People</label>
                    <input type="number" name="num_people" id="ai-people" class="form-control" value="1" required>
                </div>
                <div class="form-group">
                    <label class="form-label">Days</label>
                    <input type="number" name="days" id="ai-days" class="form-control" placeholder="7" value="7" required>
                </div>
            </div>
            
            <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 1rem;">Create Trip</button>
        </form>
    </div>
</div>
{% endblock %}
{% block scripts %}
<script>
    const dest = document.getElementById('ai-destination').value;
    if (dest) fetchCityImage(dest, 'dynamic-dest-img');
</script>
{% endblock %}''',

    'templates/dashboard.html': '''{% extends 'layout.html' %}
{% block content %}
<div style="margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: flex-end;">
    <div>
        <h1>Dashboard</h1>
        <p>Welcome back, {{ g.user.name }}! You have {{ trips|length }} upcoming adventures.</p>
    </div>
    <a href="{{ url_for('views.create_trip') }}" class="btn btn-primary">+ Generate AI Trip</a>
</div>

<div class="grid grid-3" style="margin-bottom: 3rem;">
    <div class="card">
        <h3 style="color: var(--text-muted); font-size: 0.875rem; text-transform: uppercase;">Total Trips</h3>
        <p style="font-size: 2rem; font-weight: 700; color: var(--text-main);">{{ trips|length }}</p>
    </div>
    <div class="card">
        <h3 style="color: var(--text-muted); font-size: 0.875rem; text-transform: uppercase;">AI Status</h3>
        <p style="font-size: 1.25rem; font-weight: 600; color: var(--success); margin-top: 0.5rem;">Gemini Available ✨ </p>
    </div>
</div>

<h2>Your Upcoming Trips</h2>
{% if trips %}
<div class="grid grid-2" style="margin-top: 1.5rem;">
    {% for trip in trips %}
    <div class="card" style="padding: 0; overflow: hidden; display: flex; flex-direction: column;">
        <div id="dash-trip-img-{{ loop.index }}" style="height: 150px; background: var(--card-border); background-size: cover; background-position: center;"></div>
        <div style="padding: 1.5rem;">
            <h3>{{ trip.title }}</h3>
            <p style="margin-bottom: 1rem;">Target: {{ trip.start_date.strftime('%b %d') if trip.start_date else 'Dates TBD' }}</p>
            <a href="{{ url_for('views.itinerary_view', trip_id=trip.id) }}" class="btn btn-secondary" style="width: 100%;">Manage Trip</a>
            <form action="{{ url_for('views.delete_trip', trip_id=trip.id) }}" method="POST" style="margin-top: 0.5rem;">
                <button type="submit" class="btn btn-secondary" style="width: 100%; border-color: var(--danger); color: var(--danger);">Delete Trip</button>
            </form>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="card" style="text-align: center; margin-top: 1.5rem; padding: 4rem 2rem;">
    <h3 style="margin-bottom: 1rem;">No trips created yet</h3>
    <p style="margin-bottom: 2rem;">Start building your own itinerary manually, or let our GeminiAI engine perfectly plan your route and costs.</p>
    <a href="{{ url_for('views.create_trip') }}" class="btn btn-primary">Start Planning</a>
</div>
{% endif %}
{% endblock %}
{% block scripts %}
<script>
    {% for trip in trips %}
    fetchCityImage('{{ trip.destination or trip.title }}', 'dash-trip-img-{{ loop.index }}');
    {% endfor %}
</script>
{% endblock %}''',

    'templates/city_search.html': '''{% extends 'layout.html' %}
{% block content %}
<div class="hero-header" id="city-search-header">
    <div>
        <h1>Search Global Destinations</h1>
        <p>Find inspiration anywhere in the world using OpenStreetMap's massive database.</p>
    </div>
</div>

<div class="grid" style="grid-template-columns: 1fr 1fr;">
    <div class="card" style="margin-bottom: 2rem;">
        <h3 style="margin-bottom: 1rem;">Search using OpenStreetMap</h3>
        <div style="display: flex; gap: 1rem;">
            <input type="text" id="city-input" class="form-control" placeholder="Search any city in the world..." onkeyup="searchCityMap(this.value, 'search-results')">
            <button class="btn btn-primary">Search</button>
        </div>
        <ul id="search-results" style="list-style: none; padding: 0; margin-top: 1rem; max-height: 200px; overflow-y: auto; background: var(--bg-color); border-radius: 8px;"></ul>
    </div>
    <div class="card" style="padding: 0; overflow: hidden; min-height: 300px;">
        <div id="explore-map" style="width: 100%; height: 100%; z-index: 1;"></div>
    </div>
</div>
{% endblock %}
{% block scripts %}
<script>
    fetchCityImage('Global Travel Destinations', 'city-search-header');

    // Init Map
    window.map = L.map('explore-map').setView([20.5937, 78.9629], 3); // Global view
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(window.map);

    let mapMarker = null;
    window.map.on('click', async function(e) {
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;
        
        if (mapMarker) {
            window.map.removeLayer(mapMarker);
        }
        mapMarker = L.marker([lat, lon]).addTo(window.map);
        
        const input = document.getElementById('city-input');
        input.value = 'Locating pin...';
        
        try {
            const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
            const data = await res.json();
            
            if (data && data.display_name) {
                // Try to get a clean city/state name for the input
                let shortName = data.display_name;
                if (data.address) {
                    shortName = data.address.city || data.address.town || data.address.state || data.display_name.split(',')[0];
                }
                input.value = shortName;
                
                let popupContent = `
                    <div style="text-align: center; font-family: var(--font-body);">
                        <strong style="font-size: 1.1rem;">${shortName}</strong><br>
                        <a href="/create-trip?destination=${encodeURIComponent(shortName)}" style="display: inline-block; margin-top: 10px; background: var(--accent); color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold; text-decoration: none;">Plan Trip Here</a>
                    </div>
                `;
                mapMarker.bindPopup(popupContent).openPopup();
            } else {
                input.value = 'Unknown Location';
                mapMarker.bindPopup('Unknown Location').openPopup();
            }
        } catch (err) {
            input.value = 'Error resolving location';
        }
    });
</script>
{% endblock %}'''
}

for filepath, content in files.items():
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Restored")
