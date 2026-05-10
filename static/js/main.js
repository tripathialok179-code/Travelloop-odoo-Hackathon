const UI = {
    toast: (msg, type) => {
        const root = document.getElementById('toast-root');
        if (!root) return;
        const toast = document.createElement('div');
        toast.className = `p-4 rounded-xl shadow-lg border ${type === 'error' ? 'bg-red-50 border-red-200 text-red-600' : 'bg-blue-50 border-blue-200 text-blue-600'}`;
        toast.innerText = msg;
        root.appendChild(toast);
        setTimeout(() => toast.remove(), 4000);
    }
};

async function handleCreateTrip(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const payload = Object.fromEntries(formData);

    const response = await fetch('/api/trips/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        const trip = await response.json();
        window.location.href = `/trip/workspace/${trip.id}`;
    } else {
        UI.toast("Failed to create trip. Check all fields.", "error");
    }
}

document.getElementById('create-trip-form')?.addEventListener('submit', handleCreateTrip);
