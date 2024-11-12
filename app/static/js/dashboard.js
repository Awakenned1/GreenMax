document.addEventListener('DOMContentLoaded', function() {
    const energyChartCtx = document.getElementById('energyChart').getContext('2d');
    const energyChart = new Chart(energyChartCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Energy Consumption',
                data: [],
                borderColor: '#4CAF50',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });

    function updateDashboard() {
        fetch('/api/dashboard-data')
            .then(response => response.json())
            .then(data => {
                // Update chart data
                energyChart.data.labels = data.historical.timestamps;
                energyChart.data.datasets[0].data = data.historical.values;
                energyChart.update();

                // Update real-time metrics
                document.querySelector('.metric-value').textContent = `${data.real_time.current_power} kW`;
                document.querySelector('.metric-status').textContent = data.real_time.status;
                document.querySelector('.metric-subtitle').textContent = `at ${data.real_time.peak_time}`;
                document.querySelector('.metric-value').textContent = `${data.daily_total} kWh`;
            });
    }

    // Initial update
    updateDashboard();

    // Update every 30 seconds
    setInterval(updateDashboard, 30000);
});
