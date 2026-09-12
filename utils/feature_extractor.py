import re
import ipaddress
from urllib.parse import urlparse


def extract_features(url):
    """
    Extract the 50 features used during phishing model training.
    """

    url = str(url).strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    # Remove port number
    domain_without_port = domain.split(":")[0]

    # Basic URL statistics
    url_length = len(url)
    domain_length = len(domain_without_port)

    try:
        ipaddress.ip_address(domain_without_port)
        is_domain_ip = 1
    except ValueError:
        is_domain_ip = 0

    # Character counts
    letters = sum(c.isalpha() for c in url)
    digits = sum(c.isdigit() for c in url)

    no_of_subdomain = max(
        len(domain_without_port.split(".")) - 2, 0
    )

    # Special characters
    no_of_equals = url.count("=")
    no_of_qmark = url.count("?")
    no_of_ampersand = url.count("&")

    special_chars = sum(
        not c.isalnum() for c in url
    )

    # Obfuscation indicators
    suspicious_chars = ["@", "%", "\\"]

    no_of_obfuscated_char = sum(
        url.count(char) for char in suspicious_chars
    )

    has_obfuscation = 1 if no_of_obfuscated_char > 0 else 0

    obfuscation_ratio = (
        no_of_obfuscated_char / url_length
        if url_length > 0 else 0
    )

    # Ratios
    letter_ratio = letters / url_length if url_length > 0 else 0
    digit_ratio = digits / url_length if url_length > 0 else 0
    special_char_ratio = special_chars / url_length if url_length > 0 else 0

    # HTTPS
    is_https = 1 if parsed.scheme.lower() == "https" else 0

    # URL similarity
    # Approximation because we are analyzing only the URL.
    url_similarity_index = 0.0

    # Character continuation rate
    char_continuation_rate = (
        max(len(re.findall(r"[A-Za-z0-9]", url)), 1) / max(url_length, 1)
    )

    # TLD
    tld = ""

    if "." in domain_without_port:
        tld = domain_without_port.split(".")[-1]

    tld_length = len(tld)

    # Generic approximation
    tld_legitimate_prob = 0.5

    # URL character probability approximation
    url_char_prob = letter_ratio

    # Website-content features
    # These cannot be reliably obtained from a URL alone.
    # Safe default values are used.
    line_of_code = 0
    largest_line_length = 0
    has_title = 0
    domain_title_match_score = 0
    url_title_match_score = 0
    has_favicon = 0
    robots = 0
    is_responsive = 0
    no_of_url_redirect = 0
    no_of_self_redirect = 0
    has_description = 0
    no_of_popup = 0
    no_of_iframe = 0
    has_external_form_submit = 0
    has_social_net = 0
    has_submit_button = 0
    has_hidden_fields = 0
    has_password_field = 0

    # Keyword features
    url_lower = url.lower()

    bank = 1 if any(
        word in url_lower
        for word in ["bank", "banking", "netbanking"]
    ) else 0

    pay = 1 if any(
        word in url_lower
        for word in ["pay", "payment", "paypal", "checkout"]
    ) else 0

    crypto = 1 if any(
        word in url_lower
        for word in ["crypto", "bitcoin", "ethereum", "wallet"]
    ) else 0

    has_copyright_info = 0

    # Image / CSS / JS / references
    no_of_image = 0
    no_of_css = 0
    no_of_js = 0
    no_of_self_ref = 0
    no_of_empty_ref = 0
    no_of_external_ref = 0

    # Return EXACTLY the 50 features expected by the model
    features = {
        "URLLength": url_length,
        "DomainLength": domain_length,
        "IsDomainIP": is_domain_ip,
        "URLSimilarityIndex": url_similarity_index,
        "CharContinuationRate": char_continuation_rate,
        "TLDLegitimateProb": tld_legitimate_prob,
        "URLCharProb": url_char_prob,
        "TLDLength": tld_length,
        "NoOfSubDomain": no_of_subdomain,
        "HasObfuscation": has_obfuscation,
        "NoOfObfuscatedChar": no_of_obfuscated_char,
        "ObfuscationRatio": obfuscation_ratio,
        "NoOfLettersInURL": letters,
        "LetterRatioInURL": letter_ratio,
        "NoOfDegitsInURL": digits,
        "DegitRatioInURL": digit_ratio,
        "NoOfEqualsInURL": no_of_equals,
        "NoOfQMarkInURL": no_of_qmark,
        "NoOfAmpersandInURL": no_of_ampersand,
        "NoOfOtherSpecialCharsInURL": special_chars,
        "SpacialCharRatioInURL": special_char_ratio,
        "IsHTTPS": is_https,
        "LineOfCode": line_of_code,
        "LargestLineLength": largest_line_length,
        "HasTitle": has_title,
        "DomainTitleMatchScore": domain_title_match_score,
        "URLTitleMatchScore": url_title_match_score,
        "HasFavicon": has_favicon,
        "Robots": robots,
        "IsResponsive": is_responsive,
        "NoOfURLRedirect": no_of_url_redirect,
        "NoOfSelfRedirect": no_of_self_redirect,
        "HasDescription": has_description,
        "NoOfPopup": no_of_popup,
        "NoOfiFrame": no_of_iframe,
        "HasExternalFormSubmit": has_external_form_submit,
        "HasSocialNet": has_social_net,
        "HasSubmitButton": has_submit_button,
        "HasHiddenFields": has_hidden_fields,
        "HasPasswordField": has_password_field,
        "Bank": bank,
        "Pay": pay,
        "Crypto": crypto,
        "HasCopyrightInfo": has_copyright_info,
        "NoOfImage": no_of_image,
        "NoOfCSS": no_of_css,
        "NoOfJS": no_of_js,
        "NoOfSelfRef": no_of_self_ref,
        "NoOfEmptyRef": no_of_empty_ref,
        "NoOfExternalRef": no_of_external_ref,
    }

    return features