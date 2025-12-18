// Initialize map with proper error handling
function initializeMap() {
    try {
        const map = L.map('map', {
            minZoom: 4,
            maxZoom: 19
        }).setView([20.5937, 78.9629], 5);

        // Add tile layers
        const layers = {
            'Street': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }),
            'Satellite': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Tiles © Esri'
            }),
            'Terrain': L.tileLayer('https://tile.thunderforest.com/landscape/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors, © Thunderforest'
            })
        };

        // Add default layer
        layers.Street.addTo(map);

        // Add layer control
        L.control.layers(layers).addTo(map);

        // Add scale control
        L.control.scale().addTo(map);

        // Handle map clicks
        map.on('click', async function(e) {
            const { lat, lng } = e.latlng;
            try {
                const response = await analyzeLocation(lat, lng);
                if (response.error) {
                    showError(response.message);
                } else {
                    updateDashboard(response);
                    addMarker(map, lat, lng, response);
                }
            } catch (error) {
                showError('Analysis failed. Please try again.');
            }
        });

        return map;
    } catch (error) {
        console.error('Map initialization error:', error);
        document.getElementById('map').innerHTML = 
            '<div class="error-message">Map failed to load. Please refresh the page.</div>';
        return null;
    }
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.status-panel');
    container.insertBefore(errorDiv, container.firstChild);
    
    setTimeout(() => errorDiv.remove(), 5000);
}

// Update dashboard with analysis results
function updateDashboard(data) {
    document.querySelector('.risk-score').textContent = data.risk_score;
    document.querySelector('.risk-level').textContent = data.risk_level;
    document.querySelector('.risk-recommendation').textContent = data.recommendation;
    
    // Update weather values
    document.querySelector('.temperature-value').textContent = data.temperature + '°C';
    document.querySelector('.humidity-value').textContent = data.humidity + '%';
    document.querySelector('.wind-value').textContent = data.wind_speed + ' m/s';
    document.querySelector('.rainfall-value').textContent = data.rainfall + ' mm';
}

// Add marker to map
function addMarker(map, lat, lng, data) {
    const marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup(`
        <strong>Risk Level: ${data.risk_level}</strong><br>
        Score: ${data.risk_score}<br>
        ${data.recommendation}
    `).openPopup();
}

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    const map = initializeMap();
    if (!map) {
        showError('Failed to initialize the map. Please refresh the page.');
    }
});