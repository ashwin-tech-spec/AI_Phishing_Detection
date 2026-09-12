import streamlit as st

from utils.theme import apply_theme

apply_theme()
from utils.database import get_history


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CyberShield",
    page_icon="🛡️",
    layout="wide"
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🛡️ CyberShield")

st.sidebar.markdown("### Navigation")

st.sidebar.info(
    "Use the pages on the left to detect phishing URLs, "
    "analyze suspicious websites, learn cybersecurity, "
    "and view detection history."
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🛡️ Security Modules")

st.sidebar.write("🔗 Phishing URL Detection")
st.sidebar.write("🌐 Clone Website Detection")
st.sidebar.write("🧠 Cyber Safety Quiz")
st.sidebar.write("💡 Safety Tips")
st.sidebar.write("📜 Detection History")


# =========================================================
# HOME
# =========================================================

st.title("🛡️ CyberShield")

st.subheader(
    "AI-Powered Phishing Detection & Cyber Safety Platform"
)

st.write(
    "CyberShield uses AI-based analysis to identify potentially "
    "suspicious URLs and websites while helping users learn "
    "safer online practices."
)

st.success(
    "🔐 Stay alert. Think before you click. Protect your information."
)


# =========================================================
# PROJECT STATUS
# =========================================================

st.markdown("---")

st.header("📊 Security Protection")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔗 URL Detection",
        "ACTIVE"
    )

with col2:
    st.metric(
        "🌐 Clone Detection",
        "ACTIVE"
    )

with col3:
    st.metric(
        "🧠 AI Analysis",
        "ACTIVE"
    )

with col4:
    st.metric(
        "🛡️ Cyber Safety",
        "ACTIVE"
    )


# =========================================================
# MAIN FEATURES
# =========================================================

st.markdown("---")

st.header("🚀 What CyberShield Can Do")

col1, col2 = st.columns(2)

with col1:

    st.subheader("🔗 Phishing URL Detection")

    st.write(
        "Analyze a URL using a trained machine-learning model "
        "and identify potentially suspicious characteristics."
    )

    st.info(
        "Open **URL Detection** from the sidebar."
    )


with col2:

    st.subheader("🌐 Clone Website Detection")

    st.write(
        "Analyze website-related characteristics to identify "
        "potential phishing or impersonation-style websites."
    )

    st.info(
        "Open **Clone Website Detection** from the sidebar."
    )


# =========================================================
# QUICK URL CHECKER
# =========================================================

st.markdown("---")

st.header("🔍 Quick URL Security Check")

st.write(
    "Quickly analyze a URL without opening the complete "
    "URL Detection page."
)

url = st.text_input(
    "Enter Website URL",
    placeholder="Example: https://example.com"
)

check_button = st.button(
    "🔎 Check URL",
    use_container_width=True
)


if check_button:

    if not url.strip():

        st.warning(
            "⚠️ Please enter a website URL."
        )

    else:

        try:

            from utils.predictor import predict_url

            clean_url = url.strip()

            result = predict_url(clean_url)

            prediction = result["prediction"]
            confidence = result["confidence"]

            st.markdown("---")

            # -----------------------------
            # RESULT
            # -----------------------------

            st.subheader("🔎 Analysis Result")

            if prediction == 1:

                st.error(
                    "🚨 Potential Phishing URL"
                )

                st.metric(
                    "AI Confidence",
                    f"{confidence:.2f}%"
                )

                st.warning(
                    "The model detected characteristics "
                    "associated with phishing URLs."
                )

            else:

                st.success(
                    "✅ URL Appears Safer"
                )

                st.metric(
                    "AI Confidence",
                    f"{confidence:.2f}%"
                )

                st.info(
                    "The model did not detect strong phishing "
                    "characteristics in this URL."
                )

            # -----------------------------
            # TECHNICAL DETAILS
            # -----------------------------

            with st.expander("🔎 View Technical Analysis"):

                st.write(
                    "**URL:**",
                    clean_url
                )

                st.write(
                    "**Prediction:**",
                    "Potential Phishing"
                    if prediction == 1
                    else "Appears Safer"
                )

                st.write(
                    "**Confidence:**",
                    f"{confidence:.2f}%"
                )

        except Exception as e:

            st.error(
                "❌ Unable to analyze this URL."
            )

            st.caption(
                f"Technical error: {e}"
            )


# =========================================================
# DETECTION STATISTICS
# =========================================================

st.markdown("---")

st.header("📈 Detection Statistics")

try:

    history = get_history()

    total_scans = len(history)

    phishing_scans = sum(
        1 for row in history
        if row[2] == 1
    )

    safe_scans = sum(
        1 for row in history
        if row[2] == 0
    )

    clone_scans = sum(
        1 for row in history
        if row[4] == "Clone Website Detection"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🔍 Total Scans",
            total_scans
        )

    with col2:

        st.metric(
            "🚨 Threats Detected",
            phishing_scans
        )

    with col3:

        st.metric(
            "✅ Safer Results",
            safe_scans
        )

    with col4:

        st.metric(
            "🌐 Clone Checks",
            clone_scans
        )

except Exception:

    st.warning(
        "Detection statistics are currently unavailable."
    )


# =========================================================
# RECENT ACTIVITY
# =========================================================

st.markdown("---")

st.header("🕒 Recent Detection Activity")

try:

    history = get_history()

    if len(history) == 0:

        st.info(
            "No detection history yet. "
            "Start by checking a URL."
        )

    else:

        recent_history = history[:5]

        for row in recent_history:

            detection_id = row[0]
            checked_url = row[1]
            prediction = row[2]
            confidence = row[3]
            detection_type = row[4]
            checked_at = row[5]

            if prediction == 1:

                status = "🚨 Potential Threat"

            else:

                status = "✅ Appears Safer"

            with st.container():

                col1, col2, col3 = st.columns(
                    [3, 2, 1]
                )

                with col1:

                    st.write(
                        f"**{detection_type}**"
                    )

                    st.caption(
                        checked_url
                    )

                with col2:

                    st.write(status)

                    st.caption(
                        f"Confidence: {confidence:.2f}%"
                    )

                with col3:

                    st.caption(
                        f"ID: {detection_id}"
                    )

                    st.caption(
                        checked_at
                    )

except Exception:

    st.warning(
        "Unable to load recent detection activity."
    )


# =========================================================
# HOW IT WORKS
# =========================================================

st.markdown("---")

st.header("⚙️ How CyberShield Works")

step1, step2, step3 = st.columns(3)

with step1:

    st.subheader("1️⃣ Enter")

    st.write(
        "Enter the URL of the website you want to analyze."
    )


with step2:

    st.subheader("2️⃣ Analyze")

    st.write(
        "The system extracts important URL and website "
        "characteristics and sends them to the AI model."
    )


with step3:

    st.subheader("3️⃣ Result")

    st.write(
        "CyberShield displays the prediction and confidence "
        "score to help the user understand the result."
    )


# =========================================================
# CYBERSECURITY AWARENESS
# =========================================================

st.markdown("---")

st.header("🎓 Cybersecurity Awareness")

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader("🔐 Protect Passwords")

    st.write(
        "Use strong, unique passwords and avoid sharing "
        "your passwords with others."
    )


with col2:

    st.subheader("🔗 Check Links")

    st.write(
        "Before clicking a link, check the domain name "
        "and look for suspicious characters."
    )


with col3:

    st.subheader("📱 Enable MFA")

    st.write(
        "Multi-factor authentication provides an additional "
        "layer of protection for online accounts."
    )


# =========================================================
# COMMON PHISHING WARNING SIGNS
# =========================================================

st.markdown("---")

st.header("🚨 Common Phishing Warning Signs")

warning1, warning2 = st.columns(2)

with warning1:

    st.write("🔴 **Suspicious domain names**")

    st.write("🔴 **Unexpected login requests**")

    st.write(
        "🔴 **Urgent messages asking for action**"
    )


with warning2:

    st.write(
        "🔴 **Unknown or shortened links**"
    )

    st.write(
        "🔴 **Requests for passwords or OTPs**"
    )

    st.write(
        "🔴 **Unusual spelling or website addresses**"
    )


# =========================================================
# SECURITY NOTICE
# =========================================================

st.markdown("---")

st.warning(
    "⚠️ Security Notice: AI predictions are indicators, "
    "not absolute proof that a website is safe or malicious. "
    "Always verify suspicious websites through trusted sources."
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "🛡️ CyberShield | AI-Powered Phishing Detection & "
    "Cyber Safety Platform"
)

st.caption(
    "Built for educational and cybersecurity awareness purposes."
)