from flask import Blueprint, jsonify, render_template, session
from datetime import datetime
from .services.energy_monitor import EnergyMonitoringSystem
from .services.auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        ems = EnergyMonitoringSystem()
        current_power = ems.generate_realistic_power_data()
        
        data = {
            'real_time': {
                'current_power': current_power,
                'status': 'normal' if current_power < 4.0 else 'high',
                'peak_value': current_power,
                'peak_time': datetime.now().strftime('%H:%M'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'daily_total': current_power * 24,  # Simple estimation
            'recommendations': [
                "Monitor your energy usage patterns",
                "Consider upgrading to energy-efficient appliances",
                "Set up automated controls for optimal usage"
            ],
            'historical': {
                'values': [ems.generate_realistic_power_data() for _ in range(24)],
                'timestamps': [
                    (datetime.now() - timedelta(hours=i)).strftime('%H:%M')
                    for i in range(23, -1, -1)
                ]
            }
        }
            
        return render_template('dashboard.html', data=data)
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        default_data = {
            'real_time': {
                'current_power': 0.00,
                'status': 'normal',
                'peak_value': 0.00,
                'peak_time': '--:--',
                'timestamp': 'now'
            },
            'daily_total': 0.00,
            'recommendations': [
                "Monitor your energy usage patterns",
                "Consider upgrading to energy-efficient appliances",
                "Set up automated controls for optimal usage"
            ],
            'historical': {
                'values': [],
                'timestamps': []
            }
        }
        return render_template('dashboard.html', data=default_data, error=str(e))

@main_bp.route('/api/dashboard-data')
@login_required
def get_dashboard_data():
    try:
        ems = EnergyMonitoringSystem()
        current_power = ems.generate_realistic_power_data()
        
        data = {
            'real_time': {
                'current_power': current_power,
                'status': 'normal' if current_power < 4.0 else 'high',
                'peak_value': current_power,
                'peak_time': datetime.now().strftime('%H:%M'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'daily_total': current_power * 24,
            'historical': {
                'values': [ems.generate_realistic_power_data() for _ in range(24)],
                'timestamps': [
                    (datetime.now() - timedelta(hours=i)).strftime('%H:%M')
                    for i in range(23, -1, -1)
                ]
            }
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'data': None
        }), 500
