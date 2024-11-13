// dashboard.js

class DashboardManager {
    constructor() {
        this.chart = null;
        this.updateInterval = 60000; // 1 minute
        this.init();
    }

    init() {
        this.initializeChart();
        this.setupEventListeners();
        this.startPeriodicUpdates();
        this.handleVisibilityChanges();
        this.handleOnlineOfflineStatus();
        this.addErrorHandling();
    }

    initializeChart() {
        const ctx = document.getElementById('energyChart').getContext('2d');
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Energy Usage (kW)',
                    data: [],
                    borderColor: '#FF69B4',
                    backgroundColor: 'rgba(255, 105, 180, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: 'rgba(255, 255, 255, 0.9)',
                        titleColor: '#2C3E50',
                        bodyColor: '#2C3E50',
                        borderColor: '#FF69B4',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                        callbacks: {
                            label: function(context) {
                                return `Usage: ${context.parsed.y.toFixed(2)} kW`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.1)'
                        },
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(2) + ' kW';
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                animation: {
                    duration: 750,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }

    setupEventListeners() {
        // Time range selector
        const timeRangeSelector = document.getElementById('timeRange');
        if (timeRangeSelector) {
            timeRangeSelector.addEventListener('change', (e) => {
                this.fetchData(e.target.value);
            });
        }

        // Setup metric card animations
        document.querySelectorAll('.metric-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.classList.add('highlight');
            });
            card.addEventListener('mouseleave', () => {
                card.classList.remove('highlight');
            });
        });

        // Add click event listener to refresh button
        const refreshButton = document.querySelector('.refresh-button');
        if (refreshButton) {
            refreshButton.addEventListener('click', () => {
                this.fetchData('day');
            });
        }
    }

    startPeriodicUpdates() {
        this.fetchData('day'); // Initial fetch
        setInterval(() => this.fetchData('day'), this.updateInterval);
    }

    async fetchData(timeRange = 'day') {
        try {
            const response = await fetch(`/api/dashboard-data?range=${timeRange}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            this.updateDashboard(data);
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            this.showError('Failed to update dashboard data');
        }
    }

    updateDashboard(data) {
        this.updateMetrics(data);
        this.updateChart(data);
        this.updateRecommendations(data);
        this.updateLastRefresh();
    }

    updateMetrics(data) {
        // Update current power with animation
        this.animateValue(
            '#currentPower .metric-value',
            data.real_time.current_power,
            'kW'
        );

        // Update status
        const statusElement = document.querySelector('#currentPower .metric-status');
        if (statusElement) {
            statusElement.className = `metric-status ${data.real_time.status}`;
            statusElement.textContent = this.capitalizeFirst(data.real_time.status);
        }

        // Update peak usage
        this.animateValue(
            '#peakUsage .metric-value',
            data.real_time.peak_value,
            'kW'
        );
        document.querySelector('#peakUsage .metric-subtitle').textContent = 
            `at ${data.real_time.peak_time}`;

        // Update daily usage
        this.animateValue(
            '#dailyUsage .metric-value',
            data.daily_total,
            'kWh'
        );
    }

    updateChart(data) {
        if (this.chart && data.historical) {
            this.chart.data.labels = data.historical.timestamps;
            this.chart.data.datasets[0].data = data.historical.values;
            this.chart.update('none'); // Update without animation
        }
    }

    updateRecommendations(data) {
        const container = document.getElementById('recommendationsList');
        if (container && data.recommendations) {
            container.innerHTML = data.recommendations.map(tip => `
                <div class="recommendation-item">
                    <span class="recommendation-icon"><i class="fas fa-lightbulb"></i></span>
                    <span class="recommendation-text">${tip}</span>
                </div>
            `).join('');
        }
    }

    updateLastRefresh() {
        const lastUpdate = document.getElementById('lastUpdate');
        if (lastUpdate) {
            lastUpdate.textContent = new Date().toLocaleTimeString();
        }
    }

    animateValue(selector, newValue, unit) {
        const element = document.querySelector(selector);
        if (!element) return;

        const startValue = parseFloat(element.textContent);
        const duration = 1000; // 1 second animation
        const startTime = performance.now();

        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            const currentValue = startValue + (newValue - startValue) * this.easeOutQuad(progress);
            element.textContent = `${currentValue.toFixed(2)} ${unit}`;

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        element.classList.add('updating');
        requestAnimationFrame(animate);
        setTimeout(() => element.classList.remove('updating'), duration);
    }

    easeOutQuad(x) {
        return 1 - (1 - x) * (1 - x);
    }

    capitalizeFirst(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-error';
        errorDiv.textContent = message;
        
        const dashboard = document.querySelector('.dashboard');
        if (dashboard) {
            dashboard.insertBefore(errorDiv, dashboard.firstChild);
            
            setTimeout(() => errorDiv.remove(), 5000);
        }
    }

    handleVisibilityChanges() {
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                console.log('Dashboard updates paused');
            } else {
                console.log('Dashboard updates resumed');
                window.dashboardManager?.fetchData();
            }
        });
    }

    handleOnlineOfflineStatus() {
        window.addEventListener('online', () => {
            console.log('Connection restored');
            document.querySelector('.dashboard').classList.remove('offline');
            window.dashboardManager?.fetchData();
        });

        window.addEventListener('offline', () => {
            console.log('Connection lost');
            document.querySelector('.dashboard').classList.add('offline');
        });
    }

    addErrorHandling() {
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            const dashboard = document.querySelector('.dashboard');
            if (dashboard) {
                const errorBanner = document.createElement('div');
                errorBanner.className = 'alert alert-error';
                errorBanner.textContent = 'An error occurred. Please refresh the page.';
                dashboard.insertBefore(errorBanner, dashboard.firstChild);
            }
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboardManager = new DashboardManager();
});
