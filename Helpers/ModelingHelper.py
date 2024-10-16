import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from Providers.TimeSeriesProvider import TimeSeriesProvider


def prepare_data_for_modeling(time_series: pd.Series, window_size: int):
    X, y = [], []

    for i in range(len(time_series) - window_size):
        X.append(time_series[i:i + window_size].values)
        y.append(time_series.iloc[i + window_size])

    X, y = np.array(X), np.array(y)

    # Реформування для LSTM (samples, time_steps, features)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    return X, y


def build_lstm_model(input_shape: (int, int)):
    # Визначаємо вхідний шар з конкретним input_shape
    inputs = Input(shape=input_shape)
    # Додаємо LSTM шари
    x = LSTM(100, return_sequences=True)(inputs)
    x = Dropout(0.2)(x)
    x = LSTM(100)(x)
    # Вихідний шар для прогнозування одного значення
    outputs = Dense(1)(x)
    # Створюємо модель
    model = Model(inputs, outputs)
    # Компіляція моделі
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model


class ModelingHelper:
    def __init__(self):
        self.models_path = "DB/Models"
        self.ts_provider = TimeSeriesProvider()

    def fit_model_for_data(self, ticker: str, data: pd.Series, window: int):
        X, y = prepare_data_for_modeling(data, window)

        model_path = os.path.join(self.models_path, f"model_{ticker}.keras")

        model = build_lstm_model((X.shape[1], X.shape[2]))

        checkpoint = ModelCheckpoint(model_path, save_best_only=True, monitor='loss', mode='min')
        model.fit(X, y, epochs=100, batch_size=16, callbacks=[checkpoint], verbose=0)
