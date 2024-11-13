import pytest
import tensorflow as tf
import joblib
import pandas as pd
from datetime import datetime
import numpy as np


class TestEnergyModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment before each test"""
        self.model = tf.keras.models.load_model('models/energy_model.keras')
        self.scaler = joblib.load('app/models/scaler.pkl')

    def prepare_input(self, test_data):
        """Prepare input data for prediction"""
        df = pd.DataFrame([test_data])
        df['hour'] = pd.to_datetime(df['Datetime']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['Datetime']).dt.dayofweek
        df['month'] = pd.to_datetime(df['Datetime']).dt.month

        features = [
            'Global_reactive_power', 'Voltage', 'Global_intensity',
            'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3',
            'hour', 'day_of_week', 'month'
        ]

        return df[features]

    def test_normal_load(self):
        """Test prediction with normal load"""
        test_data = {
            'Datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Global_reactive_power': 0.276,
            'Voltage': 241.68,
            'Global_intensity': 7.6,
            'Sub_metering_1': 0.0,
            'Sub_metering_2': 0.0,
            'Sub_metering_3': 0.0
        }

        input_data = self.prepare_input(test_data)
        scaled_input = self.scaler.transform(input_data)
        prediction = self.model.predict(scaled_input, verbose=0)

        print(f"\nNormal Load Test:")
        print(f"Input data: {test_data}")
        print(f"Predicted power consumption: {prediction[0][0]:.2f} kW")

        assert 0 < prediction[0][0] < 5, "Normal load prediction should be between 0 and 5 kW"

    def test_high_load(self):
        """Test prediction with high load"""
        test_data = {
            'Datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Global_reactive_power': 0.5,
            'Voltage': 235.0,
            'Global_intensity': 15.0,
            'Sub_metering_1': 1.0,
            'Sub_metering_2': 1.0,
            'Sub_metering_3': 10.0
        }

        input_data = self.prepare_input(test_data)
        scaled_input = self.scaler.transform(input_data)
        prediction = self.model.predict(scaled_input, verbose=0)

        print(f"\nHigh Load Test:")
        print(f"Input data: {test_data}")
        print(f"Predicted power consumption: {prediction[0][0]:.2f} kW")

        assert prediction[0][0] > 2, "High load prediction should be greater than 2 kW"

    def test_low_load(self):
        """Test prediction with low load"""
        test_data = {
            'Datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Global_reactive_power': 0.1,
            'Voltage': 245.0,
            'Global_intensity': 3.0,
            'Sub_metering_1': 0.0,
            'Sub_metering_2': 0.0,
            'Sub_metering_3': 0.0
        }

        input_data = self.prepare_input(test_data)
        scaled_input = self.scaler.transform(input_data)
        prediction = self.model.predict(scaled_input, verbose=0)

        print(f"\nLow Load Test:")
        print(f"Input data: {test_data}")
        print(f"Predicted power consumption: {prediction[0][0]:.2f} kW")

        assert prediction[0][0] < 2, "Low load prediction should be less than 2 kW"

    def test_input_validation(self):
        """Test input data validation"""
        test_data = {
            'Datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Global_reactive_power': 0.276,
            'Voltage': 241.68,
            'Global_intensity': 7.6,
            'Sub_metering_1': 0.0,
            'Sub_metering_2': 0.0,
            'Sub_metering_3': 0.0
        }

        input_data = self.prepare_input(test_data)
        assert len(input_data.columns) == 9, "Input should have 9 features"
        assert all(col in input_data.columns for col in [
            'Global_reactive_power', 'Voltage', 'Global_intensity',
            'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3',
            'hour', 'day_of_week', 'month'
        ]), "Missing required features"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
