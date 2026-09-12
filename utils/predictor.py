import os
import joblib
import pandas as pd

from utils.feature_extractor import extract_features


# Find project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model location
MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "phishing_model.pkl"
)

# Load trained model
model = joblib.load(MODEL_PATH)


def predict_url(url):
    """
    Analyze a URL using the trained phishing detection model.
    """

    # Extract the same 50 features used during training
    features = extract_features(url)

    # Convert dictionary to DataFrame
    feature_df = pd.DataFrame([features])

    # Get the exact feature order expected by the model
    if hasattr(model, "feature_names_in_"):
        feature_df = feature_df[
            list(model.feature_names_in_)
        ]

    # Make prediction
    prediction = int(model.predict(feature_df)[0])

    # Get probability/confidence
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(feature_df)[0]
        confidence = float(max(probabilities) * 100)
    else:
        confidence = 0.0

    return {
        "prediction": prediction,
        "confidence": confidence
    }