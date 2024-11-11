// Assuming you have a function to fetch data from your backend or API
function fetchData() {
    // Fetch data from your backend or API
    fetch('/api/ai_service')
        .then(response => response.json())
        .then(data => {
            document.getElementById('daily-consumption').textContent = data.dailyConsumption;
            document.getElementById('weekly-consumption').textContent = data.weeklyConsumption;
            document.getElementById('monthly-consumption').textContent = data.monthlyConsumption;

            // Create a Chart.js chart
            const ctx = document.getElementById('energy-chart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.timestamps,
                    datasets: [{
                        label: 'Energy Usage',
                        data: data.values,
                        borderColor: 'blue',
                        borderWidth: 1
                    }]
                },
                options: {
                    // Customize chart options as needed
                }
            });
        });
}

// Call the function to fetch and display data
fetchData();