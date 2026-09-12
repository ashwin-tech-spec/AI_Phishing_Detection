import os
import re
import joblib
import pandas as pd
from urllib.parse import urlparse


# -----------------------------
# Project paths
# -----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "clone_website_model.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR,
    "model",
    "clone_website_features.pkl"
)

BRAND_PATH = os.path.join(
    BASE_DIR,
    "model",
    "brands_reference.pkl"
)


# -----------------------------
# Load model
# -----------------------------

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_PATH)


# -----------------------------
# Load brand reference
# -----------------------------

try:
    brands_reference = joblib.load(BRAND_PATH)
except:
    brands_reference = None


# -----------------------------
# Extract domain
# -----------------------------

def get_domain(url):

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


# -----------------------------
# Detect brand in URL
# -----------------------------

def detect_brand(url):

    domain = get_domain(url)

    url_text = url.lower()

    # Common brands
    common_brands = [
        "google",
        "facebook",
        "instagram",
        "microsoft",
        "amazon",
        "apple",
        "paypal",
        "netflix",
        "linkedin",
        "github",
        "youtube",
        "flipkart",
        "sbi",
        "icici",
        "hdfc",
        "phonepe",
        "paytm"
    ]

    for brand in common_brands:

        if brand in url_text:

            return brand

    return None


# -----------------------------
# Create model features
# -----------------------------

def extract_clone_features(url):

    parsed = urlparse(url)

    domain = get_domain(url)

    path = parsed.path

    full_url = url.lower()

    features = {

        "assets_downloaded": 0,

        "remote_ip_asn": 0,

        "url_length": len(url),

        "url_dots": url.count("."),

        "url_hyphens": url.count("-"),

        "url_digits": len(
            re.findall(r"\d", url)
        ),

        "url_at_symbol": url.count("@"),

        "url_slashes": url.count("/"),

        "url_question": url.count("?"),

        "url_equals": url.count("="),

        "domain_length": len(domain),

        "domain_dots": domain.count("."),

        "domain_hyphens": domain.count("-"),

        "domain_digits": len(
            re.findall(r"\d", domain)
        ),

        "ssl_valid": 1 if parsed.scheme == "https" else 0,

        "https": 1 if parsed.scheme == "https" else 0,

        "whois_age": 0,

        "has_ip": 1 if re.match(
            r"^\d+\.\d+\.\d+\.\d+$",
            domain
        ) else 0
    }

    return features


# -----------------------------
# Main prediction function
# -----------------------------

def predict_clone_website(url):

    features = extract_clone_features(url)

    feature_df = pd.DataFrame(
        [features]
    )

    # Make sure feature order is exactly
    # the same as during training
    feature_df = feature_df[
        feature_cols
    ]

    prediction = int(
        model.predict(feature_df)[0]
    )

    # Confidence
    if hasattr(model, "predict_proba"):

        probabilities = model.predict_proba(
            feature_df
        )[0]

        confidence = float(
            max(probabilities) * 100
        )

    else:

        confidence = 0.0


    # Detect possible brand
    detected_brand = detect_brand(url)


    # -----------------------------
    # Clone decision
    # -----------------------------

    if prediction == 1 and detected_brand:

        result_text = "Clone Website Detected"

        is_clone = True

    elif prediction == 1:

        result_text = "Potential Phishing Website"

        is_clone = False

    else:

        result_text = "Likely Legitimate Website"

        is_clone = False


    return {

        "prediction": prediction,

        "confidence": confidence,

        "detected_brand": detected_brand,

        "is_clone": is_clone,

        "result": result_text,

        "features": features

    }