import numpy as np
import os
from tensorflow.keras.models import load_model


def predict_n_steps(model, last_window: np.array, n_steps: int):
    predictions = []
    current_input = last_window.reshape(1, last_window.shape[0], 1)

    for _ in range(n_steps):
        # Прогнозуємо наступне значення
        next_value = model.predict(current_input, verbose=0)[0][0]
        predictions.append(next_value)

        # Оновлюємо поточне вікно, додаючи нове значення і зсуваючи дані
        next_value_reshaped = np.array([[next_value]]).reshape(1, 1, 1)
        current_input = np.append(current_input[:, 1:, :], next_value_reshaped, axis=1)

    return predictions


class ForecastingHelper:
    def __init__(self):
        self.folder_path = "DB/Models"

    def make_forecast(self, ticker: str, last_window: np.ndarray, n_days: int):
        model_path = os.path.join(self.folder_path, f"model_{ticker}.keras")
        loaded_model = load_model(model_path)
        result = predict_n_steps(loaded_model, last_window, n_days)
        return result
