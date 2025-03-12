import joblib
import tensorflow as tf
import numpy as np
import pandas as pd

# Load the preprocessing pipeline and model
label_encoder = joblib.load("/Users/rsoedarnadi/Desktop/DataVerse/encoder.pkl")
scaler = joblib.load("/Users/rsoedarnadi/Desktop/DataVerse/scaler.pkl")
model = tf.keras.models.load_model("/Users/rsoedarnadi/Desktop/DataVerse/traffic.h5")

# Load dataset for reference
df = pd.read_csv("/Users/rsoedarnadi/Desktop/DataVerse/Traffic_Data_Department_Total.csv")
latest_year = df["Year"].max()

SEQ_LENGTH = 10  # Make sure this matches your training sequence length

def load_pipeline_and_predict(year_to_forecast):
    """
    Loads the saved pipeline and model, then predicts accident count for all departments for the given year.
    """
    forecast_results = {}
    
    for department in df["Department"].unique():
        # Retrieve department data
        dept_data = df[df["Department"] == department].reset_index(drop=True)
        dept_data = dept_data.sort_values("Year")
        
        # Ensure Accident_Count is scaled if not empty
        if not dept_data.empty:
            dept_data[["Accident_Count"]] = scaler.transform(dept_data[["Accident_Count"]])
            
            # Extract Latitude and Longitude for the department
            latitude = dept_data["Latitude"].iloc[0]
            longitude = dept_data["Longitude"].iloc[0]

            # Prepare input sequence
            last_sequence = dept_data.iloc[-SEQ_LENGTH:][["Accident_Count"]].values.reshape(1, SEQ_LENGTH, 1)
            
            predictions = []
            for _ in range(year_to_forecast - latest_year):
                pred = model.predict(last_sequence)[0, 0]
                predictions.append(pred)
                last_sequence = np.roll(last_sequence, -1)
                last_sequence[0, -1, 0] = pred

            # Convert predictions back to original scale
            if predictions:
                predictions_original = scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
            else:
                predictions_original = []

            # Create predictions dictionary with the format {year: (accident_count, latitude, longitude)}
            predictions_dict = {
                year: (pred, latitude, longitude) for year, pred in zip(range(latest_year + 1, latest_year + 1 + len(predictions_original)), predictions_original)
            }
            
            forecast_results[department] = predictions_dict
    
    return forecast_results