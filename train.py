import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import os
from utils.preprocessing import DataPreprocessor
from app.models.trainer import EnergyModel


def train_model():
    # Create directories if they don't exist
    os.makedirs('app/models', exist_ok=True)

    # Load data
    df = pd.read_csv('data/energy_data.csv')

    # Preprocess data
    preprocessor = DataPreprocessor()
    X_scaled, y, features = preprocessor.prepare_data(df)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    # Train model
    model = EnergyModel(input_dim=len(features))
    history = model.train(X_train, y_train, X_test, y_test)

    # Save model and scaler
    model.save('models/energy_model')
    joblib.dump(preprocessor.scaler, 'app/models/scaler.pkl')

    return history


if __name__ == "__main__":
    history = train_model()
