// Chart initialization
const ctx = document.getElementById('energyChart').getContext('2d');
const energyChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        datasets: [{
            label: 'Energy Usage (kWh)',
            data: [4, 3, 5, 7, 6, 4],
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
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// UI Elements
const settingsBtn = document.getElementById('settingsBtn');
const notificationsBtn = document.getElementById('notificationsBtn');
const tipsBtn = document.getElementById('tipsBtn');

// Energy Tips Handler
tipsBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/api/energy-tips');
        if (response.ok) {
            const tips = await response.json();
            alert(tips.join('\n\n'));
        }
    } catch (error) {
        console.error('Error fetching tips:', error);
        alert('Unable to load energy saving tips.');
    }
});

// Real-time Energy Updates
async function updateEnergyData() {
    try {
        const response = await fetch('/api/energy-data');
        if (response.ok) {
            const data = await response.json();
            updateChartData(data);
            updateConsumptionCards(data);
        }
    } catch (error) {
        console.error('Error updating energy data:', error);
    }
}

function updateChartData(data) {
    energyChart.data.datasets[0].data = data.hourlyUsage;
    energyChart.update();
}

function updateConsumptionCards(data) {
    document.querySelector('.consumption-card:nth-child(1) p').textContent = `${data.daily} kWh`;
    document.querySelector('.consumption-card:nth-child(2) p').textContent = `${data.weekly} kWh`;
    document.querySelector('.consumption-card:nth-child(3) p').textContent = `${data.monthly} kWh`;
}

// Start real-time updates
setInterval(updateEnergyData, 60000); // Update every minute
updateEnergyData(); // Initial update
