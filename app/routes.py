from flask import Blueprint, jsonify, render_template, session, request, redirect, url_for, flash
from datetime import datetime, timedelta
from .services.energy_monitor import EnergyMonitoringSystem
from .services.auth import login_required
from .models import User
from . import db, logger, fcm_manager

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
        user_id = session.get('user_id')
        data = ems.get_dashboard_data(user_id=user_id)
        
        # Get user's energy settings
        user = User.query.get(user_id)
        energy_settings = user.energy_settings if user else {}
        
        return render_template('dashboard.html', 
                             data=data, 
                             energy_settings=energy_settings)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        default_data = {
            'real_time': {
                'current_power': 0.00,
                'status': 'normal',
                'peak_value': 0.00,
                'peak_time': '--:--',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        return render_template('dashboard.html', 
                             data=default_data, 
                             error=str(e))

@main_bp.route('/api/dashboard-data')
@login_required
def get_dashboard_data():
    try:
        ems = EnergyMonitoringSystem()
        data = ems.get_dashboard_data(user_id=session.get('user_id'))
        return jsonify(data)
    except Exception as e:
        logger.error(f"API dashboard data error: {e}")
        return jsonify({
            'error': str(e),
            'data': None
        }), 500

@main_bp.route('/profile')
@login_required
def profile():
    try:
        user = User.query.get(session.get('user_id'))
        if not user:
            return redirect(url_for('auth.login'))
        
        return render_template('profile.html', 
                             user=user.to_dict())
    except Exception as e:
        logger.error(f"Profile error: {e}")
        return render_template('profile.html', 
                             error="Failed to load profile information")

@main_bp.route('/settings')
@login_required
def settings():
    try:
        user = User.query.get(session.get('user_id'))
        if not user:
            return redirect(url_for('auth.login'))
        
        return render_template('settings.html',
                             notification_settings=user.get_notification_settings(),
                             energy_settings=user.energy_settings)
    except Exception as e:
        logger.error(f"Settings error: {e}")
        return render_template('settings.html', 
                             error="Failed to load settings")

@main_bp.route('/api/update-settings', methods=['POST'])
@login_required
def update_settings():
    try:
        user = User.query.get(session.get('user_id'))
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json
        
        # Update notification preferences
        if 'notification_preferences' in data:
            user.update_notification_preferences(data['notification_preferences'])
        
        # Update energy settings
        if 'energy_settings' in data:
            user.update_energy_settings(data['energy_settings'])
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Settings updated successfully',
            'settings': user.get_notification_settings()
        })
    except Exception as e:
        logger.error(f"Settings update error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/api/update-fcm-token', methods=['POST'])
@login_required
def update_fcm_token():
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'No token provided'}), 400
        
        user = User.query.get(session.get('user_id'))
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.update_fcm_token(token)
        
        return jsonify({
            'status': 'success',
            'message': 'FCM token updated successfully'
        })
    except Exception as e:
        logger.error(f"FCM token update error: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/logout')
@login_required
def logout():
    try:
        # Update last login time
        user = User.query.get(session.get('user_id'))
        if user:
            user.last_login = datetime.utcnow()
            db.session.commit()
        
        session.clear()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('auth.login'))
    except Exception as e:
        logger.error(f"Logout error: {e}")
        session.clear()
        return redirect(url_for('auth.login'))

@main_bp.route('/api/analysis')
@login_required
def get_analysis():
    try:
        ems = EnergyMonitoringSystem()
        analysis = ems.get_interpretable_data_analysis(session.get('user_id'))
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return jsonify({
            'error': str(e),
            'data': None
        }), 500

# Error handlers
@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Utility routes
@main_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

@main_bp.before_request
def before_request():
    session.permanent = True
    session.modified = True
