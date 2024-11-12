# app/services/background_task.py

import time
from .energy_monitor import EnergyMonitoringSystem
from .firebase_service import update_firebase_data

def start_background_task():
    ems = EnergyMonitoringSystem()
    while True:
        data = ems.get_dashboard_data(user_id=1)
        if data:
            update_firebase_data(data)
        time.sleep(30)  # Update every 30 seconds
