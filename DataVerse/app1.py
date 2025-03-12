from flask import Flask, render_template, jsonify
import numpy as np
import pandas as pd
import tensorflow as tf

app = Flask(__name__)

# Load trained LSTM model
#model = tf.keras.models.load_model("lstm_traffic_model.h5")

# Dummy function to simulate prediction
def predict_accidents():
    # Simulated locations (latitude, longitude) and forecasted accident severity
    accident_data = [
        {"lat": 40.7128, "lon": -74.0060, "severity": np.random.randint(1, 5)},  # New York
        {"lat": 34.0522, "lon": -118.2437, "severity": np.random.randint(1, 5)},  # Los Angeles
        {"lat": 41.8781, "lon": -87.6298, "severity": np.random.randint(1, 5)},  # Chicago
    ]
    return accident_data

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict():
    results = predict_accidents()
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
