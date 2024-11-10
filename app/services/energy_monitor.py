from datetime import datetime, timedelta
import numpy as np


class EnergyMonitoringSystem:
    def __init__(self):
        self.peak_threshold = 4.0

    def get_dashboard_data(self, user_id, time_range='day'):
        """Generate dashboard data"""
        try:
            # Generate current data
            current_data = self._generate_current_data()

            # Generate historical data
            historical_data = self._generate_historical_data(time_range)

            # Generate recommendations
            recommendations = self._generate_recommendations(current_data)

            return {
                'real_time': current_data,
                'historical': historical_data,
                'recommendations': recommendations,
                'daily_total': round(sum(historical_data['values'][-24:]), 2)
            }
        except Exception as e:
            print(f"Error generating dashboard data: {e}")
            return None

    def _generate_current_data(self):
        """Generate real-time data"""
        current_hour = datetime.now().hour

        # Simulate power consumption based on time of day
        if current_hour >= 23 or current_hour < 5:
            power = np.random.uniform(0.1, 0.8)
            status = 'low'
        elif 5 <= current_hour < 9:
            power = np.random.uniform(1.0, 2.5)
            status = 'high'
        else:
            power = np.random.uniform(0.5, 1.5)
            status = 'medium'

        return {
            'current_power': round(power, 2),
            'peak_value': round(power * 1.2, 2),
            'peak_time': f"{current_hour:02d}:00",
            'status': status,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def _generate_historical_data(self, time_range):
        """Generate historical data"""
        if time_range == 'day':
            hours = 24
        elif time_range == 'week':
            hours = 168
        else:
            hours = 24  # Default to day

        timestamps = []
        values = []

        current_time = datetime.now()
        for i in range(hours):
            past_time = current_time - timedelta(hours=i)
            power = np.random.uniform(0.5, 3.0)

            timestamps.append(past_time.strftime('%Y-%m-%d %H:%M'))
            values.append(round(power, 2))

        return {
            'timestamps': list(reversed(timestamps)),
            'values': list(reversed(values))
        }

    def _generate_recommendations(self, current_data):
        """Generate energy-saving recommendations"""
        recommendations = [
            "Monitor your energy usage patterns",
            "Consider upgrading to energy-efficient appliances",
            "Set up automated controls for optimal usage"
        ]

        if current_data['status'] == 'high':
            recommendations.append("Reduce power usage during peak hours")

        return recommendations
