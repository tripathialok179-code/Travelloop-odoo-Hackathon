// Function to handle Create Trip Form (API Integration)
document.getElementById('create-trip-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch('/api/trips', { // cite: 14
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const trip = await response.json();
            window.location.href = `/trip/workspace/${trip.id}`;
        } else {
            const error = await response.json();
            UI.toast(`Error: ${error.message}`, 'error');
        }
    } catch (err) {
        UI.toast("Network error. Please try again.", "error");
    }
});

// Animation logic for elements appearing on scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) entry.target.classList.add('animate-fade-in');
    });
}, { threshold: 0.1 });

document.querySelectorAll('.glass').forEach(el => observer.observe(el));