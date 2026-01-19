"""
Module de prédiction pour le nombre de vélos comptés à Tours.
"""

import pandas as pd
import joblib
from pathlib import Path


class BikeCountPredictor:
    """Prédicteur du nombre de vélos comptés basé sur un modèle RandomForest."""

    def __init__(self, model_path):
        """
        Initialize the predictor with a trained model.

        Parameters
        ----------
        model_path : str or Path
            Path to the saved model file (joblib format)
        """
        self.model_path = Path(model_path)
        self.model = None
        self.load_model()

    def load_model(self):
        """Load the trained model from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        self.model = joblib.load(self.model_path)

    def predict(
        self,
        t2m_min,
        t2m_max,
        tp_total,
        sd_total,
        i10fg_max,
        sf_max,
        is_weekend,
        is_holiday,
        is_school_vacation,
    ):
        """
        Predict the number of bikes counted for given features.

        Parameters
        ----------
        t2m_min : float
            Minimum temperature in Celsius
        t2m_max : float
            Maximum temperature in Celsius
        tp_total : float
            Total precipitation in meters
        sd_total : float
            Snow depth in meters
        i10fg_max : float
            Maximum wind gust in m/s
        sf_max : float
            Maximum snow fall in meters
        is_weekend : int
            0 for weekday, 1 for weekend
        is_holiday : int
            0 if not holiday, 1 if holiday
        is_school_vacation : int
            0 if not school vacation, 1 if school vacation

        Returns
        -------
        int
            Predicted number of bikes counted
        """
        features = pd.DataFrame(
            {
                "t2m_min": [float(t2m_min)],
                "t2m_max": [float(t2m_max)],
                "tp_total": [float(tp_total)],
                "sd_total": [float(sd_total)],
                "i10fg_max": [float(i10fg_max)],
                "sf_max": [float(sf_max)],
                "is_weekend": [int(is_weekend)],
                "is_holiday": [int(is_holiday)],
                "is_school_vacation": [int(is_school_vacation)],
            }
        )

        prediction = self.model.predict(features)
        return int(round(prediction[0]))

    def predict_batch(self, df):
        """
        Predict for multiple rows in a DataFrame.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with feature columns

        Returns
        -------
        np.ndarray
            Array of predictions
        """
        predictions = self.model.predict(df)
        return (predictions.round()).astype(int)
