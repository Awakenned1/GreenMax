import random
from datetime import datetime, timedelta
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, db
import os
import numpy as np
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

    def get_ai_recommendations(self, usage_data):
        """Generate AI recommendations for improving energy efficiency."""
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
            Format as a bullet-pointed list.
            """

            response = self.model.generate_content(prompt)
            recommendations = [
                line.strip('• ').strip() 
                for line in response.text.split('\n') 
                if line.strip()
            ][:3]

            return recommendations
        except Exception as e:
            print(f"AI recommendation error: {e}")
            return [
                "Monitor your energy usage patterns",
                "Consider upgrading to energy-efficient appliances",
                "Set up automated controls for optimal usage"
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
            
            # Set current data and add to historical
            user_ref.child('current').set(current_data)
            user_ref.child('historical').push(current_data)
            
            # Save recommendations
            if 'recommendations' in data:
                user_ref.child('recommendations').set(data['recommendations'])
            
            return True
        except Exception as e:
            print(f"Firebase save error: {e}")
            return False

    def get_dashboard_data(self, user_id):
        """Fetch data to be displayed on the dashboard."""
        try:
            # Generate current power data
            current_power = self.generate_realistic_power_data()
            
            # Update peak values if current exceeds the previous peak
            if current_power > self.peak_value:
                self.peak_value = current_power
                self.peak_time = datetime.now().strftime('%H:%M')

            # Determine current power status
            status = 'high' if current_power > 4.0 else 'low' if current_power < 1.0 else 'normal'

            # Safely get historical data from Firebase
            try:
                historical_ref = self.db.reference(f'users/{user_id}/energy_data/historical')
                historical_data = historical_ref.get() if historical_ref else {}
                historical_list = list(historical_data.values()) if historical_data else []
            except Exception as firebase_error:
                print(f"Firebase error: {firebase_error}")
                historical_list = []

            # Calculate daily total energy consumption
            today = datetime.now().strftime('%Y-%m-%d')
            today_data = [
                entry for entry in historical_list 
                if entry.get('timestamp', '').startswith(today)
            ]
            daily_total = (
                sum(float(entry.get('power', 0)) for entry in today_data) / len(today_data)
                if today_data else 0
            )

            # Prepare data structure
            data = {
                'real_time': {
                    'current_power': current_power,
                    'peak_value': self.peak_value,
                    'peak_time': self.peak_time,
                    'status': status,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                },
                'historical': {
                    'timestamps': [entry.get('timestamp') for entry in historical_list[-24:]],
                    'values': [float(entry.get('power', 0)) for entry in historical_list[-24:]]
                },
                'daily_total': round(daily_total, 2),
                'recommendations': [
                    "Monitor your energy usage patterns",
                    "Consider upgrading to energy-efficient appliances",
                    "Set up automated controls for optimal usage"
                ]
            }

            # Get AI recommendations if possible
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

            # Save updated data to Firebase
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
                    "Monitor your energy usage patterns",
                    "Consider upgrading to energy-efficient appliances",
                    "Set up automated controls for optimal usage"
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
