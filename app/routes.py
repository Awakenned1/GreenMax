from flask import Blueprint, render_template, jsonify, session, redirect, url_for
from functools import wraps

main_bp = Blueprint('main', __name__)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/dashboard')
@login_required  # Add this decorator to protect the route
def index():
    # Mock data for the dashboard
    dashboard_data = {
        # Energy Overview
        'daily_consumption': 24.5,
        'weekly_consumption': 168.3,
        'monthly_consumption': 720.8,
        'daily_trend': -5,
        'weekly_trend': 2,
        'monthly_trend': -1,

        # Real-time Tracking
        'current_power': 450,
        'peak_time': '14:00',
        'peak_value': 3.2,

        # Energy Tips
        'energy_tips': [
            "Switch to LED bulbs to save up to 75% on lighting costs",
            "Use smart power strips to eliminate phantom energy usage",
            "Optimize thermostat settings: 68°F in winter, 78°F in summer",
            "Regular HVAC maintenance can improve efficiency by 15%"
        ],

        # Cost Tips
        'cost_tips': [
            "Run major appliances during off-peak hours",
            "Install a programmable thermostat",
            "Use natural light when possible",
            "Seal air leaks around windows and doors"
        ],

        # Connected Devices
        'devices': [
            {
                'id': '1',
                'name': 'Living Room AC',
                'status': 'active',
                'consumption': 1.2,
                'icon': 'M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'
            },
            {
                'id': '2',
                'name': 'Kitchen Refrigerator',
                'status': 'active',
                'consumption': 0.8,
                'icon': 'M3 3h18v18H3zM9 3v18M15 3v18'
            },
            {
                'id': '3',
                'name': 'Bedroom Light',
                'status': 'inactive',
                'consumption': 0.1,
                'icon': 'M15 5h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-2'
            }
        ],

        # Chart Data
        'chart_labels': ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        'chart_data': [4, 3, 5, 7, 6, 4]
    }

    return render_template('index.html', **dashboard_data)

@main_bp.route('/api/device/<device_id>')
@login_required  # Protect API endpoints too
def get_device_status(device_id):
    # Mock device status
    return jsonify({'status': 'on' if device_id in ['1', '2'] else 'off'})

@main_bp.route('/api/device/<device_id>/toggle', methods=['POST'])
@login_required  # Protect API endpoints
def toggle_device(device_id):
    # Mock device toggle
    return jsonify({'success': True})

@main_bp.route('/api/energy-data')
@login_required  # Protect API endpoints
def get_energy_data():
    # Mock energy data
    return jsonify({
        'labels': ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
        'values': [4, 3, 5, 7, 6, 4]
    })
