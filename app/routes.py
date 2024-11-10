from flask import Blueprint, jsonify, render_template, session
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
        data = ems.get_dashboard_data(user_id=1)
        if data is None:
            data = {
                'real_time': {
                    'current_power': 0.00,
                    'peak_value': 0.00,
                    'peak_time': '--:--',
                    'status': 'normal',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'historical': {
                    'timestamps': [],
                    'values': []
                },
                'recommendations': [],
                'daily_total': 0.00
            }
        return render_template('dashboard.html', **data)
    except Exception as e:
        print(f"Dashboard error: {e}")
        return render_template('dashboard.html', error=str(e))

@main_bp.route('/api/dashboard-data')
@login_required
def get_dashboard_data():
    try:
        ems = EnergyMonitoringSystem()
        data = ems.get_dashboard_data(user_id=1)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
