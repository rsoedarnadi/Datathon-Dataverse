from flask import Flask, request, jsonify, render_template
import pandas as pd
from pipeline import load_pipeline_and_predict

app = Flask(__name__)

# Load department names
df = pd.read_csv("/Users/rsoedarnadi/Desktop/DataVerse/Traffic_Data_Department_Total.csv")
departments = sorted(df["Department"].unique())  # Assuming the original names are stored

@app.route("/")
def home():
    return render_template("index.html", departments=departments)

@app.route("/predict", methods=["POST"])
def predict():
    """
    Receives user input, runs the prediction, and returns the results.
    """
    data = request.json
    year_to_forecast = int(data.get("year"))

    forecast_results = load_pipeline_and_predict(year_to_forecast)
    
    # Prepare the results to include latitude and longitude, and convert predictions to float
    results_with_coordinates = {
        dept: [
            {
                "year": year,
                "accident_count": float(count),  # Convert to float
                "latitude": float(lat),          # Convert to float
                "longitude": float(lon)          # Convert to float
            } for year, (count, lat, lon) in predictions.items()
        ] for dept, predictions in forecast_results.items()
    }

    return jsonify(results_with_coordinates)

if __name__ == "__main__":
    app.run(debug=True)