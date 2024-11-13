import tensorflow as tf
import joblib
import os

class EnergyPredictor:
    def __init__(self, model_path='models/energy_model', scaler_path='models/scaler.pkl'):
        try:
            self.model = tf.keras.models.load_model(model_path)
            self.scaler = joblib.load(scaler_path)
            print("Model and scaler loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.scaler = None

    def predict(self, data):
        try:
            if self.model is None or self.scaler is None:
                return None
            # Transform data and make prediction
            scaled_data = self.scaler.transform([list(data.values())])
            prediction = self.model.predict(scaled_data)
            return float(prediction[0][0])
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

# Initialize predictor instance
predictor = EnergyPredictor()
