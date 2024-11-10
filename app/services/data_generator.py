from datetime import datetime, timedelta
import numpy as np


def generate_energy_data():
    """Generate realistic energy consumption data"""
    current_time = datetime.now()
    current_hour = current_time.hour
    day_of_week = current_time.weekday()

    # Get base load and status
    base_load, status = _get_base_load(current_hour)

    # Apply adjustments
    base_load = _apply_adjustments(base_load, current_hour, day_of_week)

    # Calculate power
    power = base_load * np.random.uniform(0.9, 1.1)

    return {
        'current_power': round(power, 2),
        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
        'status': status,
        'peak_time': f"{19 if day_of_week < 5 else 15}:00",
        'peak_value': round(power * 1.2, 2)
    }


def _get_base_load(hour):
    """Determine base load based on time of day"""
    if hour >= 23 or hour < 5:  # Night
        return np.random.uniform(0.1, 0.8), 'low'
    elif 5 <= hour < 9:  # Morning peak
        return np.random.uniform(1.0, 2.5), 'high'
    elif 17 <= hour < 22:  # Evening peak
        return np.random.uniform(1.5, 3.0), 'high'
    else:  # Regular hours
        return np.random.uniform(0.5, 1.5), 'medium'


def _apply_adjustments(base_load, hour, day_of_week):
    """Apply various adjustments to base load"""
    # Weekend adjustment
    if day_of_week >= 5:
        base_load *= 1.2

    # Temperature adjustment
    temperature = 20 + np.sin(hour / 12 * np.pi) * 5
    weather_factor = 1.0 + (temperature - 20) * 0.05

    return base_load * weather_factor
