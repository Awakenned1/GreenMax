import pandas as pd
from sklearn.preprocessing import StandardScaler


class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()

    def prepare_data(self, df):
        # Convert datetime
        df['Datetime'] = pd.to_datetime(df['Datetime'])

        # Extract time features
        df['hour'] = df['Datetime'].dt.hour
        df['day_of_week'] = df['Datetime'].dt.dayofweek
        df['month'] = df['Datetime'].dt.month

        # Select features
        features = [
            'Global_reactive_power', 'Voltage', 'Global_intensity',
            'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3',
            'hour', 'day_of_week', 'month'
        ]
        target = 'Global_active_power'

        # Split features and target
        X = df[features]
        y = df[target]

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        return X_scaled, y, features

    def transform_input(self, input_data):
        return self.scaler.transform(input_data)
