import os
import re
import joblib
import pandas as pd
from urllib.parse import urlparse


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR, "model", "clone_website_model.pkl"
)

FEATURE_PATH = os.path.join(
    BASE_DIR, "model", "clone_website_features.pkl"
)

BRAND_PATH = os.path.join(
    BASE_DIR, "model", "brands_reference.pkl"
)


# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = joblib.load(MODEL_PATH)
feature_cols = joblib.load(FEATURE_PATH)


# --------------------------------------------------
# LOAD BRAND REFERENCE
# --------------------------------------------------

try:
    brands_reference = joblib.load(BRAND_PATH)
except Exception:
    brands_reference = {}


# --------------------------------------------------
# GET DOMAIN
# --------------------------------------------------

def get_domain(url):
    """
    Extract the hostname from a URL.
    """

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    domain = parsed.netloc.lower().split(":")[0]

    if domain.startswith("www."):
        domain = domain[4:]

    return domain


# --------------------------------------------------
# NORMALIZE BRAND TEXT
# --------------------------------------------------

def normalize_text(text):
    """
    Convert brand text into simple alphanumeric form.
    """

    return re.sub(r"[^a-z0-9]", "", str(text).lower())


# --------------------------------------------------
# CHECK OFFICIAL WEBSITE
# --------------------------------------------------

def is_official_domain(domain, official_url):
    """
    Check whether the entered domain is the official
    brand domain or a subdomain of it.
    """

    if not official_url:
        return False

    official_domain = get_domain(official_url)

    if domain == official_domain:
        return True

    if domain.endswith("." + official_domain):
        return True

    return False


# --------------------------------------------------
# DETECT BRAND
# --------------------------------------------------

def detect_brand(url):
    """
    Detect a brand from the domain using brands_reference.pkl.

    Returns:
        {
            name,
            website,
            category,
            description,
            is_official
        }
    """

    domain = get_domain(url)

    # First check official websites
    for key, info in brands_reference.items():

        if not isinstance(info, dict):
            continue

        official_website = info.get("website", "")

        if is_official_domain(domain, official_website):

            return {
                "name": info.get("name", key),
                "website": official_website,
                "category": info.get("category", ""),
                "description": info.get("description", ""),
                "is_official": True
            }

    # Check suspicious brand impersonation
    domain_parts = domain.split(".")

    for key, info in brands_reference.items():

        if not isinstance(info, dict):
            continue

        brand_name = info.get("name", key)

        possible_names = {
            normalize_text(key),
            normalize_text(brand_name)
        }

        for brand in possible_names:

            if not brand:
                continue

            for part in domain_parts:

                normalized_part = normalize_text(part)

                if brand == normalized_part or (
                    len(brand) >= 4 and brand in normalized_part
                ):

                    return {
                        "name": brand_name,
                        "website": info.get("website", ""),
                        "category": info.get("category", ""),
                        "description": info.get("description", ""),
                        "is_official": False
                    }

    return None


# --------------------------------------------------
# EXTRACT CLONE FEATURES
# --------------------------------------------------

def extract_clone_features(url):

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    domain = get_domain(url)

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

        # Runtime approximation.
        # This does NOT verify the SSL certificate.
        "ssl_valid": 1 if parsed.scheme == "https" else 0,

        "https": 1 if parsed.scheme == "https" else 0,

        # These values require additional website/WHOIS
        # information which we are not collecting here.
        "whois_age": 0,

        "has_ip": 1 if re.match(
            r"^\d+\.\d+\.\d+\.\d+$",
            domain
        ) else 0
    }

    return features


# --------------------------------------------------
# MAIN PREDICTION FUNCTION
# --------------------------------------------------

def predict_clone_website(url):

    features = extract_clone_features(url)

    feature_df = pd.DataFrame([features])

    # Make sure the feature order exactly matches
    # the trained model.
    feature_df = feature_df[feature_cols]

    # ML prediction
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

    # Brand detection
    brand_info = detect_brand(url)

    detected_brand = None
    legitimate_website = None
    brand_is_official = False

    if brand_info:

        detected_brand = brand_info["name"]

        legitimate_website = brand_info["website"]

        brand_is_official = brand_info["is_official"]


    # --------------------------------------------------
    # FINAL DECISION
    # --------------------------------------------------

    # Official brand website should NEVER be classified
    # as a clone simply because the ML model predicted 1.
    if brand_is_official:

        final_prediction = 0
        is_clone = False

        result_text = "Official / Legitimate Website"

    elif prediction == 1 and detected_brand:

        final_prediction = 1
        is_clone = True

        result_text = "Clone / Brand Impersonation Detected"

    elif prediction == 1:

        final_prediction = 1
        is_clone = False

        result_text = "Potential Phishing Website"

    else:

        final_prediction = 0
        is_clone = False

        result_text = "Likely Legitimate Website"


    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {

        "prediction": final_prediction,

        "confidence": confidence,

        "detected_brand": detected_brand,

        "legitimate_website": legitimate_website,

        "is_clone": is_clone,

        "brand_is_official": brand_is_official,

        "result": result_text,

        "features": features
    }
