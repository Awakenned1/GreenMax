class DashboardManager {
    constructor(initialData) {
        this.chart = null;
        this.initialData = initialData;
        this.updateInterval = 60000; // 1 minute
    }

    initialize() {
        console.log('Initializing dashboard...'); // Debug log
        this.initializeChart();
        this.setupEventListeners();
        this.startAutoUpdate();
    }

    initializeChart() {
        const ctx = document.getElementById('energyChart');
        if (!ctx) {
            console.error('Chart canvas not found');
            return;
        }

        console.log('Creating chart with data:', this.initialData); // Debug log

        this.chart = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: this.initialData.historical.timestamps,
                datasets: [{
                    label: 'Energy Usage (kW)',
                    data: this.initialData.historical.values,
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Power (kW)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    setupEventListeners() {
        const timeRange = document.getElementById('timeRange');
        if (timeRange) {
            timeRange.addEventListener('change', (e) => {
                this.updateTimeRange(e.target.value);
            });
        }
    }

    startAutoUpdate() {
        setInterval(() => this.updateDashboard(), this.updateInterval);
    }

    async updateDashboard() {
        try {
            const response = await fetch('/api/dashboard-data');
            const data = await response.json();

            if (data.error) {
                console.error('API Error:', data.error);
                return;
            }

            this.updateMetrics(data.real_time);
            this.updateChart(data.historical);
        } catch (error) {
            console.error('Error updating dashboard:', error);
        }
    }

    updateMetrics(realTimeData) {
        const elements = {
            'current-power': realTimeData.current_power + ' kW',
            'peak-value': realTimeData.peak_value + ' kW',
            'peak-time': realTimeData.peak_time,
            'status': realTimeData.status
        };

        for (const [id, value] of Object.entries(elements)) {
            const element = document.querySelector(`[data-metric="${id}"]`);
            if (element) {
                element.textContent = value;
            }
        }
    }

    updateChart(historicalData) {
        if (this.chart && historicalData.timestamps && historicalData.values) {
            this.chart.data.labels = historicalData.timestamps;
            this.chart.data.datasets[0].data = historicalData.values;
            this.chart.update();
        }
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking for dashboard...'); // Debug log
    if (document.getElementById('energyChart')) {
        console.log('Dashboard found, initializing...'); // Debug log
        const dashboard = new DashboardManager(window.DASHBOARD_DATA || {
            historical: { timestamps: [], values: [] },
            real_time: {}
        });
        dashboard.initialize();
    }
});
