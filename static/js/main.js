
// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const target = current === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', target);
    localStorage.setItem('theme', target);
    updateThemeIcon(target);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if(icon) {
        icon.innerHTML = theme === 'light' ? '🌙' : '☀️';
    }
}

document.addEventListener('DOMContentLoaded', initTheme);

// Unsplash Dynamic Image Fetching
async function fetchCityImage(cityName, imgElementId) {
    try {
        const response = await fetch(`/api/unsplash/city?city=${encodeURIComponent(cityName)}`);
        const data = await response.json();
        const imgEl = document.getElementById(imgElementId);
        if (imgEl) {
            imgEl.style.backgroundImage = `url('${data.url}')`;
        }
    } catch (e) {
        console.error("Failed to fetch image", e);
    }
}

// Nominatim OpenStreetMap Search
async function searchCityMap(query, resultListId) {
    if(!query || query.length < 3) return;
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
        const data = await res.json();
        const list = document.getElementById(resultListId);
        list.innerHTML = '';
        data.forEach(place => {
            const li = document.createElement('li');
            li.style.padding = '0.5rem';
            li.style.borderBottom = '1px solid var(--border)';
            li.style.cursor = 'pointer';
            li.innerText = place.display_name;
            li.onclick = () => {
                const shortCity = place.display_name.split(',')[0];
                window.location.href = `/create-trip?destination=${encodeURIComponent(shortCity)}`;
            };
            list.appendChild(li);
        });
    } catch (e) {
        console.error("Nominatim error", e);
    }
}

// Gemini AI Suggestion (Used in creation or dashboard)
async function getAISuggestion(destination, days, start_point, transport_mode, vehicle_model, num_people, resultDivId) {
    const resultDiv = document.getElementById(resultDivId);
    resultDiv.innerHTML = '<p>✨ Analyzing complex routes and calculating costs via Gemini AI...</p>';
    try {
        const res = await fetch('/api/gemini/suggest', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({destination, days, start_point, transport_mode, vehicle_model, num_people})
        });
        const data = await res.json();
        if(res.ok) {
            let html = `<h3>Estimated Cost: ₹ ${data.total_budget_inr.toLocaleString()}</h3>`;
            html += `<ul style="margin-top:1rem; padding-left:1.5rem;">`;
            data.itinerary.forEach(day => { html += `<li style="margin-bottom:0.75rem">${day}</li>`; });
            html += `</ul>`;
            resultDiv.innerHTML = html;
        } else {
            resultDiv.innerHTML = `<p style="color:var(--danger)">Error: ${data.error}</p>`;
        }
    } catch (e) { resultDiv.innerHTML = `<p style="color:var(--danger)">Network Error</p>`; }
}

// Manage Trip - AI Summary
async function generateTripSummary(trip_id, resultDivId) {
    const resultDiv = document.getElementById(resultDivId);
    resultDiv.innerHTML = '<p style="color: var(--accent); font-weight: 500;">✨ Gemini is generating a destination summary and transportation advice...</p>';
    try {
        const res = await fetch('/api/gemini/manage_summary', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({trip_id: trip_id})
        });
        const data = await res.json();
        if(res.ok) {
            let html = `<p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem;">${data.summary}</p>`;
            html += `<div style="background: rgba(0,0,0,0.05); padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                <h4 style="color: var(--accent); margin-bottom: 0.5rem;">✨ Best Time To Visit</h4>
                <p>${data.best_time_to_visit}</p>
            </div>
            <h4>Transportation Options</h4>
            <ul style="margin-top: 0.5rem; padding-left: 1.5rem; color: var(--text-muted);">`;
            data.transportation_options.forEach(opt => { html += `<li style="margin-bottom: 0.5rem;">${opt}</li>`; });
            html += `</ul>`;
            resultDiv.innerHTML = html;
        } else { resultDiv.innerHTML = `<p style="color:var(--danger)">Error: ${data.error}</p>`; }
    } catch(e) { resultDiv.innerHTML = `<p style="color:var(--danger)">Network Error</p>`; }
}

// Manage Trip - AI Budget
async function generateTripBudget(trip_id, resultDivId) {
    const resultDiv = document.getElementById(resultDivId);
    resultDiv.innerHTML = '<p style="color: var(--accent); font-weight: 500;">✨ Gemini is calculating budget tiers and specific cost breakdowns...</p>';
    try {
        const res = await fetch('/api/gemini/manage_budget', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({trip_id: trip_id})
        });
        const data = await res.json();
        if(res.ok) {
            renderBudgetOptions(data.budget_tiers || data, trip_id, resultDivId);
        } else { resultDiv.innerHTML = `<p style="color:var(--danger)">Error: ${data.error}</p>`; }
    } catch(e) { resultDiv.innerHTML = `<p style="color:var(--danger)">Network Error</p>`; }
}

function renderBudgetOptions(budget_tiers, trip_id, resultDivId) {
    const resultDiv = document.getElementById(resultDivId);
    let html = `<div class="grid grid-3" style="gap: 1rem; margin-bottom: 1.5rem;">`;
    budget_tiers.forEach(tier => {
        html += `<div class="card" style="padding: 1.5rem;">
            <p style="text-transform: uppercase; font-size: 0.8rem; font-weight: bold; color: var(--text-muted);">${tier.tier_name}</p>
            <h3 style="color: var(--accent); font-size: 1.5rem;">₹ ${tier.total_cost}</h3>
            <p style="font-size: 0.8rem; margin-bottom: 1rem;">Total Trip</p>
            <ul style="font-size: 0.85rem; color: var(--text-muted); padding-left: 1rem; margin-bottom: 1rem; list-style:none;">
                <li>🍔 Food: ₹${tier.breakdown.food}</li>
                <li>🚗 Trans: ₹${tier.breakdown.transport}</li>
                <li>🏨 Stay: ₹${tier.breakdown.accommodation}</li>
                <li>🎟️ Acts: ₹${tier.breakdown.activities}</li>
            </ul>
            <button class="btn btn-primary" style="width:100%" onclick="selectBudgetTier(${trip_id}, '${encodeURIComponent(JSON.stringify(tier))}')">Select This Plan</button>
        </div>`;
    });
    html += `</div>`;
    resultDiv.innerHTML = html;
}

async function selectBudgetTier(trip_id, tierStr) {
    const selected_tier = JSON.parse(decodeURIComponent(tierStr));
    try {
        const res = await fetch('/api/trip/save_budget', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({trip_id, selected_tier})
        });
        if(res.ok) window.location.reload();
    } catch(e) { console.error(e); }
}

// Manage Trip - AI Packing
async function generatePackingList(trip_id, resultDivId) {
    const resultDiv = document.getElementById(resultDivId);
    resultDiv.innerHTML = '<p style="color: var(--accent); font-weight: 500;">✨ Gemini is analyzing the climate and compiling your essentials...</p>';
    try {
        const res = await fetch('/api/gemini/packing', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({trip_id: trip_id})
        });
        const data = await res.json();
        if(res.ok) {
            window.currentPackingList = data.packing_items || [];
            renderPackingList(resultDivId);
        } else { resultDiv.innerHTML = `<p style="color:var(--danger)">Error: ${data.error}</p>`; }
    } catch(e) { resultDiv.innerHTML = `<p style="color:var(--danger)">Network Error</p>`; }
}

function renderPackingList(resultDivId) {
    const resultDiv = document.getElementById(resultDivId);
    let html = `<ul style="list-style:none; padding:0; margin-top:1rem;">`;
    window.currentPackingList.forEach((item, index) => {
        html += `<li style="display:flex; justify-content:space-between; padding:0.75rem; background:var(--bg-color); border:1px solid var(--border); border-radius:8px; margin-bottom:0.5rem;">
            <span>${item}</span>
            <button onclick="removePackingItem(${index}, '${resultDivId}')" style="background:none; border:none; color:var(--danger); cursor:pointer;">❌</button>
        </li>`;
    });
    html += `</ul>
    <div style="display:flex; gap:0.5rem; margin-top:1rem;">
        <input type="text" id="manual-packing-item" class="form-control" placeholder="Add custom item...">
        <button class="btn btn-secondary" onclick="addPackingItem('${resultDivId}')">Add</button>
    </div>`;
    resultDiv.innerHTML = html;
}

function removePackingItem(index, resultDivId) {
    window.currentPackingList.splice(index, 1);
    renderPackingList(resultDivId);
    savePackingToDB();
}

function addPackingItem(resultDivId) {
    const input = document.getElementById('manual-packing-item');
    if(input && input.value.trim() !== '') {
        window.currentPackingList.push(input.value.trim());
        renderPackingList(resultDivId);
        savePackingToDB();
        input.value = '';
    }
}

async function savePackingToDB() {
    try {
        await fetch("/api/trip/save_packing", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({trip_id: window.currentTripId, items: window.currentPackingList})
        });
    } catch(e) {}
}

// Manage Trip - AI Travel Logistics
async function generateTravelLogistics(trip_id, resultDivId) {
    const resultDiv = document.getElementById(resultDivId);
    try {
        const res = await fetch('/api/gemini/route_logistics', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({trip_id: trip_id})
        });
        const data = await res.json();
        if(res.ok) {
            let html = `<p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">${data.logistics_summary}</p>`;
            html += `<h4>Detailed Insights</h4><ul style="margin-top: 0.5rem; padding-left: 1.5rem; color: var(--text-muted);">`;
            data.insights.forEach(opt => { html += `<li style="margin-bottom: 0.5rem;">${opt}</li>`; });
            html += `</ul>`;
            resultDiv.innerHTML = html;
        } else { resultDiv.innerHTML = `<p style="color:var(--danger)">Error: ${data.error}</p>`; }
    } catch(e) { resultDiv.innerHTML = `<p style="color:var(--danger)">Network Error</p>`; }
}
