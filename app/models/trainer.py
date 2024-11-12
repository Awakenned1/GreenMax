import tensorflow as tf
from tensorflow import keras
layers = keras.layers
models = keras.models
import os


class EnergyModel:
    def __init__(self, input_dim):
        self.model = self._build_model(input_dim)

    def _build_model(self, input_dim):
        inputs = tf.keras.Input(shape=(input_dim,))
        x = layers.Dense(64, activation='relu')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(32, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.2)(x)
        x = layers.Dense(16, activation='relu')(x)
        outputs = layers.Dense(1)(x)

        model = models.Model(inputs=inputs, outputs=outputs)

        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )

        return model

    def train(self, X_train, y_train, X_val, y_val, epochs=50):
        callback = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )

        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=[callback],
            verbose=1
        )
        return history

    def save(self, path):
        # Ensure the directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # Save the model with .keras extension
        self.model.save(f"{path}.keras")
