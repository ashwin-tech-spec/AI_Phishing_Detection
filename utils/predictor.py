
import os
import joblib
import pandas as pd
from urllib.parse import urlparse

from utils.feature_extractor import extract_features


# ---------------------------------------------------------
# Load existing phishing model
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_model.pkl")

model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# Basic brand/domain risk check
# ---------------------------------------------------------

COMMON_BRANDS = [
    "google",
    "microsoft",
    "apple",
    "amazon",
    "paypal",
    "facebook",
    "instagram",
    "whatsapp",
    "netflix",
    "linkedin",
    "twitter",
    "github",
    "yahoo",
    "bank",
    "sbi",
    "hdfc",
    "icici",
    "axis"
]


def brand_domain_check(url):
    """
    Checks whether a known brand name appears in the domain
    while the domain does not look like the official brand domain.

    This is only an additional risk signal.
    It does NOT replace the ML model.
    """

    clean_url = str(url).strip()

    if not clean_url.startswith(("http://", "https://")):
        clean_url = "https://" + clean_url

    parsed = urlparse(clean_url)
    domain = parsed.netloc.lower().split(":")[0]

    # Remove www.
    if domain.startswith("www."):
        domain = domain[4:]

    for brand in COMMON_BRANDS:

        if brand in domain:

            # Official-looking domains
            official_domains = [
                f"{brand}.com",
                f"{brand}.in",
                f"{brand}.org",
                f"{brand}.net"
            ]

            if domain in official_domains:
                return False

            # Brand appears inside another domain
            return True

    return False


# ---------------------------------------------------------
# Main URL prediction function
# ---------------------------------------------------------

def predict_url(url):

    # Extract the same 50 features used by the ML model
    features = extract_features(url)

    feature_df = pd.DataFrame([features])

    # Make sure feature order matches the trained model
    if hasattr(model, "feature_names_in_"):
        feature_df = feature_df[list(model.feature_names_in_)]

    # ML prediction
    ml_prediction = int(model.predict(feature_df)[0])

    # ML confidence
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(feature_df)[0]
        ml_confidence = float(max(probabilities) * 100)
    else:
        ml_confidence = 0.0

    # Additional brand/domain check
    brand_risk = brand_domain_check(url)

    # -----------------------------------------------------
    # Final decision
    # -----------------------------------------------------

    if ml_prediction == 1 or brand_risk:
        final_prediction = 1
    else:
        final_prediction = 0

    # Confidence is kept from the ML model.
    # The brand check is only an additional risk signal.
    final_confidence = ml_confidence

    return {
        "prediction": final_prediction,
        "confidence": final_confidence,
        "brand_risk": brand_risk,
        "ml_prediction": ml_prediction
    }
