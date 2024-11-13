from flask import Blueprint, jsonify, render_template, session
from datetime import datetime, timedelta
from .services.energy_monitor import EnergyMonitoringSystem
from .services.auth import login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('home.html')


@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main_bp.route('/terms')
def terms():
    return render_template('terms.html')



@main_bp.route('/dashboard')
@login_required
def dashboard():
    try:
        ems = EnergyMonitoringSystem()
        # Fetch data from Firebase using user_id from session
        data = ems.get_dashboard_data(user_id=session.get('user_id', 1))

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
        # Fetch data from Firebase using user_id from session
        data = ems.get_dashboard_data(user_id=session.get('user_id', 1))

        return jsonify(data)
    except Exception as e:
        return jsonify({
            'error': str(e),
            'data': None
        }), 500

@main_bp.route('/profile')
@login_required
def profile():
    try:
        # Here you would get the user's profile information from the database
        user_info = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'joined': '2023-02-01'
        }
        return render_template('profile.html', user=user_info)
    except Exception as e:
        print(f"Profile error: {str(e)}")
        return render_template('profile.html', error="Failed to load profile information")

@main_bp.route('/settings')
@login_required
def settings():
    try:
        # Placeholder for settings page, where users can modify their preferences
        return render_template('settings.html')
    except Exception as e:
        print(f"Settings error: {str(e)}")
        return render_template('settings.html', error="Failed to load settings")

@main_bp.route('/api/update-settings', methods=['POST'])
@login_required
def update_settings():
    try:
        # Logic for updating user settings goes here
        return jsonify({'status': 'success', 'message': 'Settings updated successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@main_bp.route('/logout')
@login_required
def logout():
    # Logic for logging out the user
    session.clear()
    return render_template('logout.html', message="You have been logged out successfully.")
