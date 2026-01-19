"""
Example usage of the BikeCountPredictor module.

This script demonstrates how to use the predictor outside of Streamlit.
"""

from predictor import BikeCountPredictor
from pathlib import Path

# Initialize the predictor
model_path = Path(__file__).parent.parent / "data" / "bike_count_model.pkl"
predictor = BikeCountPredictor(model_path)

# Example 1: Single prediction
print("=== Single Prediction ===")
prediction = predictor.predict(
    t2m_min=-5.0,
    t2m_max=10.0,
    tp_total=0.001,
    sd_total=0.0,
    i10fg_max=5.0,
    sf_max=0.0,
    is_weekend=0,
    is_holiday=0,
    is_school_vacation=0,
)
print(f"Predicted bikes: {prediction}")

# Example 2: Batch prediction from CSV
print("\n=== Batch Prediction ===")
import pandas as pd

df = pd.DataFrame(
    {
        "t2m_min": [-5.0, 0.0, -10.0],
        "t2m_max": [10.0, 15.0, 5.0],
        "tp_total": [0.001, 0.0, 0.01],
        "sd_total": [0.0, 0.0, 0.5],
        "i10fg_max": [5.0, 3.0, 8.0],
        "sf_max": [0.0, 0.0, 0.1],
        "is_weekend": [0, 1, 0],
        "is_holiday": [0, 0, 1],
        "is_school_vacation": [0, 0, 0],
    }
)

predictions = predictor.predict_batch(df)
print(f"Predictions: {predictions}")

# Add to dataframe and display
df["predicted_bikes"] = predictions
print(df)
