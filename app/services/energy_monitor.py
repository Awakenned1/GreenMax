import random
import re
from datetime import datetime, timedelta
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, db
import os
import numpy as np
from firebase_admin import messaging
from sklearn.preprocessing import MinMaxScaler
from dotenv import load_dotenv

load_dotenv()

class EnergyMonitoringSystem:
    def __init__(self):
        # Initialize Firebase
        if not firebase_admin._apps:
            cred = credentials.Certificate("Service-key.json")
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
            })
        
        # Initialize Gemini AI Model
        try:
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Warning: Could not initialize Gemini: {e}")
            self.model = None
        
        self.scaler = MinMaxScaler()
        self.last_update = datetime.now()
        self.peak_value = 0.0
        self.peak_time = '--:--'
        self.db = db

 # Add notification thresholds
        self.notification_thresholds = {
            'high_usage': 4.0,  # kW
            'peak_alert': 4.5,  # kW
            'daily_limit': 50.0  # kWh
        }
        # Define recommendation symbols
        self.recommendation_symbols = {
            'efficiency': '⚡',
            'cost': '💰',
            'schedule': '⏰',
            'upgrade': '🔄',
            'alert': '⚠️',
            'eco': '🌱',
            'smart': '🤖',
            'temperature': '🌡️',
            'lighting': '💡',
            'power': '🔌'
        }

        # Define status icons
        self.status_icons = {
            'high': '🔴',
            'normal': '🟢',
            'low': '🟡'
        }



# Track notification status to prevent spam
        self.last_notification_time = {}

    def send_push_notification(self, user_id, title, body, data=None):
        """Send push notification using Firebase Cloud Messaging."""
        try:
            # Check if enough time has passed since last notification (15 minutes)
            current_time = datetime.now()
            if (user_id in self.last_notification_time and 
                (current_time - self.last_notification_time[user_id]).total_seconds() < 900):
                return False

            # Get user's FCM token from Firebase
            user_ref = self.db.reference(f'users/{user_id}')
            fcm_token = user_ref.child('fcm_token').get()
            
            if not fcm_token:
                print(f"No FCM token found for user {user_id}")
                return False

            # Construct message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data if data else {},
                token=fcm_token,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        icon='energy_icon',
                        color='#2d8bac',
                        sound='default'
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound='default',
                            badge=1
                        )
                    )
                )
            )

            # Send message
            response = messaging.send(message)
            
            # Update last notification time
            self.last_notification_time[user_id] = current_time
            
            # Log notification
            self._log_notification(user_id, title, body, response)
            
            return True

        except Exception as e:
            print(f"Error sending push notification: {e}")
            return False

    def _log_notification(self, user_id, title, body, response):
        """Log notification details to Firebase."""
        try:
            notification_data = {
                'timestamp': datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
                'title': title,
                'body': body,
                'status': 'sent',
                'response': response
            }
            
            self.db.reference(f'users/{user_id}/notifications').push(notification_data)
        
        except Exception as e:
            print(f"Error logging notification: {e}")

    def check_and_notify(self, user_id, current_power, daily_total):
        """Check thresholds and send notifications if needed."""
        notifications = []

        # Check high usage
        if current_power > self.notification_thresholds['high_usage']:
            notifications.append({
                'title': '⚠️ High Power Usage Alert',
                'body': f'Current power usage ({current_power}kW) exceeds normal levels. Tap to view details.',
                'data': {'type': 'high_usage', 'value': str(current_power)}
            })

        # Check peak alert
        if current_power > self.notification_thresholds['peak_alert']:
            notifications.append({
                'title': '🔴 Peak Power Alert',
                'body': f'Critical power usage detected ({current_power}kW). Immediate action recommended.',
                'data': {'type': 'peak_alert', 'value': str(current_power)}
            })

        # Check daily limit
        if daily_total > self.notification_thresholds['daily_limit']:
            notifications.append({
                'title': '📊 Daily Usage Alert',
                'body': f'Daily energy consumption ({daily_total}kWh) has exceeded the recommended limit.',
                'data': {'type': 'daily_limit', 'value': str(daily_total)}
            })

        # Send notifications
        for notification in notifications:
            self.send_push_notification(
                user_id,
                notification['title'],
                notification['body'],
                notification['data']
            )

    def generate_realistic_power_data(self):
        """Generate realistic power consumption values based on the time of day."""
        current_hour = datetime.now().hour
        if 0 <= current_hour < 6:
            base_load = random.uniform(0.3, 0.8)
        elif 6 <= current_hour < 9:
            base_load = random.uniform(2.0, 4.0)
        elif 9 <= current_hour < 17:
            base_load = random.uniform(1.0, 2.5)
        elif 17 <= current_hour < 22:
            base_load = random.uniform(2.5, 4.5)
        else:
            base_load = random.uniform(0.8, 1.5)
        
        noise = random.uniform(-0.2, 0.2)
        return round(max(0.1, min(5.0, base_load + noise)), 2)

    def clean_text(self, text):
        """Clean and format recommendation text."""
        # Remove special characters and extra spaces
        cleaned = re.sub(r'[*"""]', '', text)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()

        # Identify recommendation type based on keywords
        text_lower = cleaned.lower()
        rec_type = 'efficiency'  # default type
        
        keyword_mapping = {
            'cost|save|bill|expense': 'cost',
            'schedule|time|peak|hour': 'schedule',
            'upgrade|replace|install': 'upgrade',
            'warning|alert|critical|high': 'alert',
            'eco|green|environment': 'eco',
            'smart|automat|control': 'smart',
            'temperature|heat|cool': 'temperature',
            'light|led|bulb': 'lighting',
            'power|energy|consumption': 'power'
        }

        for pattern, type_ in keyword_mapping.items():
            if re.search(pattern, text_lower):
                rec_type = type_
                break

        # Add appropriate symbol
        symbol = self.recommendation_symbols.get(rec_type, '💡')
        
        # Format final text
        formatted = f"{symbol} {cleaned}"
        
        # Capitalize first letter after symbol
        formatted = re.sub(r'^(.*?\s)(.)', lambda m: f"{m.group(1)}{m.group(2).upper()}", formatted)

        return formatted

    def get_ai_recommendations(self, usage_data):
        """Generate AI recommendations with cleaned and formatted text."""
        try:
            if not self.model:
                raise Exception("Gemini model not initialized")

            prompt = f"""
            As an energy efficiency expert, analyze this energy usage data:
            - Current Power: {usage_data['current_power']} kW
            - Daily Total: {usage_data['daily_total']} kWh
            - Peak Value: {usage_data['peak_value']} kW at {usage_data['peak_time']}
            - Status: {usage_data['status']}

            Provide 3 specific, actionable recommendations to improve energy efficiency.
            Each recommendation should be clear and concise.
            Focus on: energy saving, cost reduction, or smart automation.
            Keep each recommendation under 100 characters.
            """

            response = self.model.generate_content(prompt)
            recommendations = [
                self.clean_text(line.strip('• ').strip()) 
                for line in response.text.split('\n') 
                if line.strip()
            ][:3]

            return recommendations

        except Exception as e:
            print(f"AI recommendation error: {e}")
            return [
                self.clean_text("Monitor and optimize peak hour energy usage"),
                self.clean_text("Switch to energy-efficient LED lighting"),
                self.clean_text("Install smart thermostats for temperature control")
            ]

    def save_to_firebase(self, user_id, data):
        """Save energy data to Firebase."""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            user_ref = self.db.reference(f'users/{user_id}/energy_data')
            
            current_data = {
                'timestamp': timestamp,
                'power': data['real_time']['current_power'],
                'status': data['real_time']['status'],
                'peak_value': data['real_time']['peak_value'],
                'peak_time': data['real_time']['peak_time'],
                'daily_total': data['daily_total']
            }
            
            user_ref.child('current').set(current_data)
            user_ref.child('historical').push(current_data)
            
            if 'recommendations' in data:
                user_ref.child('recommendations').set(data['recommendations'])
            
            return True
        except Exception as e:
            print(f"Firebase save error: {e}")
            return False

    def get_dashboard_data(self, user_id):
        """Fetch data to be displayed on the dashboard."""
        try:
            current_power = self.generate_realistic_power_data()
            
            if current_power > self.peak_value:
                self.peak_value = current_power
                self.peak_time = datetime.now().strftime('%H:%M')

            status = 'high' if current_power > 4.0 else 'low' if current_power < 1.0 else 'normal'
            formatted_status = f"{self.status_icons[status]} {status.title()}"

            try:
                historical_ref = self.db.reference(f'users/{user_id}/energy_data/historical')
                historical_data = historical_ref.get() if historical_ref else {}
                historical_list = list(historical_data.values()) if historical_data else []
            except Exception as firebase_error:
                print(f"Firebase error: {firebase_error}")
                historical_list = []

            today = datetime.now().strftime('%Y-%m-%d')
            today_data = [
                entry for entry in historical_list 
                if entry.get('timestamp', '').startswith(today)
            ]
            daily_total = (
                sum(float(entry.get('power', 0)) for entry in today_data)
            ) * 0.25  # Assuming data points are collected every 15 minutes

            data = {
                'real_time': {
                    'current_power': current_power,
                    'peak_value': self.peak_value,
                    'peak_time': self.peak_time,
                    'status': formatted_status,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'historical': {
                    'timestamps': [entry.get('timestamp') for entry in historical_list[-24:]],
                    'values': [float(entry.get('power', 0)) for entry in historical_list[-24:]]
                },
                'daily_total': round(daily_total, 2),
                'recommendations': [
                    self.clean_text("Monitor your energy usage patterns"),
                    self.clean_text("Consider upgrading to energy-efficient appliances"),
                    self.clean_text("Set up automated controls for optimal usage")
                ]
            }

            try:
                ai_recommendations = self.get_ai_recommendations({
                    'current_power': current_power,
                    'daily_total': daily_total,
                    'peak_value': self.peak_value,
                    'peak_time': self.peak_time,
                    'status': status
                })
                if ai_recommendations:
                    data['recommendations'] = ai_recommendations
            except Exception as ai_error:
                print(f"AI recommendation error: {ai_error}")

            try:
                self.save_to_firebase(user_id, data)
            except Exception as save_error:
                print(f"Firebase save error: {save_error}")

            return data
            
        except Exception as e:
            print(f"Error in get_dashboard_data: {e}")
            return {
                'real_time': {
                    'current_power': 0.00,
                    'status': 'normal',
                    'peak_value': 0.00,
                    'peak_time': '--:--',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'daily_total': 0.00,
                'recommendations': [
                    self.clean_text("Monitor your energy usage patterns"),
                    self.clean_text("Consider upgrading to energy-efficient appliances"),
                    self.clean_text("Set up automated controls for optimal usage")
                ],
                'historical': {
                    'values': [],
                    'timestamps': []
                }
            }

    def get_historical_data(self, user_id):
        """Retrieve historical energy consumption data."""
        try:
            historical_ref = self.db.reference(f'users/{user_id}/energy_data/historical').get()
            if not historical_ref:
                return {'timestamps': [], 'values': []}
            
            historical_data = list(historical_ref.values())
            return {
                'timestamps': [entry['timestamp'] for entry in historical_data],
                'values': [entry['power'] for entry in historical_data]
            }
        except Exception as e:
            print(f"Error getting historical data: {e}")
            return {'timestamps': [], 'values': []}

    def get_interpretable_data_analysis(self, user_id):
        """Provide interpretable analysis of energy consumption patterns."""
        try:
            historical_data = self.get_historical_data(user_id)
            if not historical_data['values']:
                return None

            # Structure the data for analysis
            structured_data = {
                'power_values': np.array(historical_data['values']),
                'timestamps': [datetime.strptime(ts, '%Y-%m-%d_%H:%M:%S') 
                             for ts in historical_data['timestamps']]
            }

            # Calculate key metrics
            analysis = {
                'patterns': {
                    'peak_hours': self._analyze_peak_hours(structured_data),
                    'daily_trends': self._analyze_daily_trends(structured_data),
                    'efficiency_score': self._calculate_efficiency_score(structured_data)
                },
                'interpretations': self._generate_interpretations(structured_data)
            }

            return analysis

        except Exception as e:
            print(f"Error in interpretable analysis: {e}")
            return None

    def _analyze_peak_hours(self, data):
        """Analyze peak usage hours with interpretable results."""
        try:
            hours = [ts.hour for ts in data['timestamps']]
            power_by_hour = {}
            
            for hour, power in zip(hours, data['power_values']):
                if hour not in power_by_hour:
                    power_by_hour[hour] = []
                power_by_hour[hour].append(power)

            peak_hours = {
                hour: {
                    'average_power': np.mean(values),
                    'frequency': len(values),
                    'interpretation': '🔴 High Usage' if np.mean(values) > 3.0 else 
                                   '🟡 Medium Usage' if np.mean(values) > 1.5 else 
                                   '🟢 Low Usage'
                }
                for hour, values in power_by_hour.items()
            }

            return peak_hours

        except Exception as e:
            print(f"Error in peak hours analysis: {e}")
            return {}

    def _analyze_daily_trends(self, data):
        """Analyze daily consumption trends with interpretable insights."""
        try:
            daily_power = {}
            for ts, power in zip(data['timestamps'], data['power_values']):
                date = ts.date()
                if date not in daily_power:
                    daily_power[date] = []
                daily_power[date].append(power)

            trends = {
                date.strftime('%Y-%m-%d'): {
                    'total_consumption': sum(values),
                    'average_power': np.mean(values),
                    'peak_value': max(values),
                    'efficiency_rating': '⚡ Efficient' if np.mean(values) < 2.0 else 
                                      '⚠️ Review Usage' if np.mean(values) < 3.5 else 
                                      '❗ High Consumption'
                }
                for date, values in daily_power.items()
            }

            return trends

        except Exception as e:
            print(f"Error in daily trends analysis: {e}")
            return {}

    def _calculate_efficiency_score(self, data):
        """Calculate an interpretable efficiency score."""
        try:
            avg_power = np.mean(data['power_values'])
            peak_power = max(data['power_values'])
            variance = np.var(data['power_values'])

            # Normalize components
            avg_score = 1 - min(avg_power / 5.0, 1)  # 5.0 is max expected power
            peak_score = 1 - min(peak_power / 5.0, 1)
            stability_score = 1 - min(variance / 2.0, 1)  # 2.0 is max expected variance

            # Calculate weighted score
            efficiency_score = (avg_score * 0.4 + peak_score * 0.3 + stability_score * 0.3) * 100

            return {
                'score': round(efficiency_score, 1),
                'rating': '🌟 Excellent' if efficiency_score >= 80 else
                         '✨ Good' if efficiency_score >= 60 else
                         '📊 Average' if efficiency_score >= 40 else
                         '⚠️ Needs Improvement',
                'components': {
                    'average_usage': f"{round(avg_score * 100, 1)}%",
                    'peak_management': f"{round(peak_score * 100, 1)}%",
                    'stability': f"{round(stability_score * 100, 1)}%"
                }
            }

        except Exception as e:
            print(f"Error in efficiency score calculation: {e}")
            return None

    def _generate_interpretations(self, data):
        """Generate human-readable interpretations of the data."""
        try:
            avg_power = np.mean(data['power_values'])
            peak_power = max(data['power_values'])
            
            interpretations = []
            
            # Power usage interpretation
            if avg_power > 3.0:
                interpretations.append("🔴 High average power consumption detected")
            elif avg_power > 1.5:
                interpretations.append("🟡 Moderate power consumption observed")
            else:
                interpretations.append("🟢 Efficient power consumption maintained")

            # Peak usage interpretation
            if peak_power > 4.0:
                interpretations.append("⚠️ Significant peak usage detected - consider load balancing")
            
            # Add time-based patterns
            peak_hours = self._analyze_peak_hours(data)
            high_usage_hours = [
                hour for hour, data in peak_hours.items() 
                if data['interpretation'] == '🔴 High Usage'
            ]
            
            if high_usage_hours:
                interpretations.append(
                    f"⏰ Peak usage typically occurs during hours: {', '.join(map(str, high_usage_hours))}"
                )

            return interpretations

        except Exception as e:
            print(f"Error generating interpretations: {e}")
            return []

# Example usage
if __name__ == "__main__":
    energy_system = EnergyMonitoringSystem()
    
    # Get dashboard data
    user_id = "example_user"
    dashboard_data = energy_system.get_dashboard_data(user_id)
    print("Dashboard Data:")
    print(dashboard_data)

    # Get historical data
    historical_data = energy_system.get_historical_data(user_id)
    print("\nHistorical Data:")
    print(historical_data)

    # Generate realistic power data
    current_power = energy_system.generate_realistic_power_data()
    print(f"\nCurrent Power: {current_power} kW")

    # Get AI recommendations
    ai_recommendations = energy_system.get_ai_recommendations({
        'current_power': current_power,
        'daily_total': dashboard_data['daily_total'],
        'peak_value': dashboard_data['real_time']['peak_value'],
        'peak_time': dashboard_data['real_time']['peak_time'],
        'status': dashboard_data['real_time']['status']
    })
    print("\nAI Recommendations:")
    for rec in ai_recommendations:
        print(rec)
