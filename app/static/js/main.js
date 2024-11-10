// Initialize Chart.js
let energyChart;

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Chart
    initializeChart();

    // Initialize Device Controls
    initializeDeviceControls();

    // Initialize Time Range Selector
    initializeTimeRangeSelector();

    // Initialize Power Indicators
    updatePowerIndicators();

    // Start Periodic Updates
    startPeriodicUpdates();
});

// Chart Initialization
function initializeChart() {
    const ctx = document.getElementById('energyChart').getContext('2d');
    energyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Energy Usage (kWh)',
                data: [],
                borderColor: '#4ade80',
                tension: 0.4,
                fill: true,
                backgroundColor: 'rgba(74, 222, 128, 0.1)'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Energy Usage (kWh)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time'
                    }
                }
            }
        }
    });
}

// Device Controls
function initializeDeviceControls() {
    document.querySelectorAll('.device-toggle').forEach(button => {
        button.addEventListener('click', async () => {
            const deviceId = button.dataset.id;
            try {
                const response = await fetch(`/api/device/${deviceId}/toggle`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                if (response.ok) {
                    updateDeviceStatus(deviceId);
                } else {
                    console.error('Failed to toggle device');
                }
            } catch (error) {
                console.error('Error toggling device:', error);
            }
        });

        // Initial status check
        updateDeviceStatus(button.dataset.id);
    });
}

// Update Device Status
async function updateDeviceStatus(id) {
    try {
        const response = await fetch(`/api/device/${id}`);
        const data = await response.json();

        const deviceCard = document.querySelector(`[data-id="${id}"]`).closest('.device-card');
        const statusElement = deviceCard.querySelector('.device-status');
        const button = deviceCard.querySelector('.device-toggle');

        statusElement.textContent = data.status === 'on' ? 'active' : 'inactive';
        statusElement.className = `device-status ${data.status === 'on' ? 'active' : 'inactive'}`;
        button.textContent = data.status === 'on' ? 'Turn Off' : 'Turn On';
    } catch (error) {
        console.error('Error updating device status:', error);
    }
}

// Time Range Selector
function initializeTimeRangeSelector() {
    document.getElementById('timeRange').addEventListener('change', async (e) => {
        const range = e.target.value;
        try {
            const response = await fetch(`/api/energy-data?range=${range}`);
            const data = await response.json();
            updateChart(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    });
}

// Update Chart Data
function updateChart(data) {
    energyChart.data.labels = data.labels;
    energyChart.data.datasets[0].data = data.values;
    energyChart.update();
}

// Power Indicators
function updatePowerIndicators() {
    document.querySelectorAll('.power-indicator').forEach(indicator => {
        const value = parseFloat(indicator.dataset.value);
        const maxPower = 1000; // Maximum power in watts
        const percentage = (value / maxPower) * 100;

        indicator.style.width = `${Math.min(percentage, 100)}%`;
        indicator.style.backgroundColor = getColorForPower(percentage);
    });
}

// Get Color Based on Power Usage
function getColorForPower(percentage) {
    if (percentage < 30) return '#4ade80'; // Green
    if (percentage < 70) return '#fbbf24'; // Yellow
    return '#ef4444'; // Red
}

// Tips Button Functionality
document.getElementById('tipsBtn')?.addEventListener('click', () => {
    const tipsContainer = document.querySelector('.recommendations-grid');
    tipsContainer.classList.toggle('expanded');
    const button = document.getElementById('tipsBtn');
    button.textContent = tipsContainer.classList.contains('expanded') ? 'Show Less' : 'View More Tips';
});

// Periodic Updates
function startPeriodicUpdates() {
    setInterval(async () => {
        try {
            // Update energy data
            const response = await fetch('/api/energy-data');
            const data = await response.json();
            updateChart(data);

            // Update power indicators
            updatePowerIndicators();

            // Update device statuses
            document.querySelectorAll('.device-toggle').forEach(button => {
                updateDeviceStatus(button.dataset.id);
            });
        } catch (error) {
            console.error('Error updating data:', error);
        }
    }, 30000); // Update every 30 seconds
}

// Error Handling
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-error';
    errorDiv.textContent = message;

    document.querySelector('.dashboard').prepend(errorDiv);

    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}
