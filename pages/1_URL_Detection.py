import streamlit as st

from utils.predictor import predict_url
from utils.database import save_detection


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Phishing URL Detection",
    page_icon="🔗",
    layout="wide"
)


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.url-header {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.url-subtitle {
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 25px;
}

.input-box {
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-top: 15px;
    margin-bottom: 20px;
}

.result-box {
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-top: 20px;
}

.safe-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(0,128,0,0.25);
}

.warning-box {
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(200,100,0,0.25);
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="url-header">🔗 Phishing URL Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="url-subtitle">'
    'Analyze a website URL using our machine-learning model '
    'and identify potentially suspicious links.'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------
# Security Notice
# -----------------------------
st.info(
    "🛡️ Enter only the URL. Never enter passwords, OTPs, "
    "banking PINs, or other sensitive information."
)


# -----------------------------
# URL Input
# -----------------------------
st.markdown(
    '<div class="input-box">',
    unsafe_allow_html=True
)

st.subheader("🌐 Enter Website URL")

url = st.text_input(
    "Website URL",
    placeholder="https://example.com",
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Analyze Button
# -----------------------------
if st.button(
    "🔍 Analyze URL",
    use_container_width=True
):

    if not url.strip():

        st.warning("⚠️ Please enter a website URL.")

    else:

        clean_url = url.strip()

        # Add https if user did not provide protocol
        if not clean_url.lower().startswith(
            ("http://", "https://")
        ):
            clean_url = "https://" + clean_url

        try:

            # -----------------------------
            # AI Prediction
            # -----------------------------
            with st.spinner("🤖 AI is analyzing the URL..."):

                result = predict_url(clean_url)


            # -----------------------------
            # Save to Database
            # -----------------------------
            save_detection(
                url=clean_url,
                prediction=result["prediction"],
                confidence=result["confidence"],
                detection_type="URL Detection"
            )


            # -----------------------------
            # Result Section
            # -----------------------------
            st.divider()

            st.subheader("🔎 Analysis Result")


            prediction = result["prediction"]
            confidence = result["confidence"]


            # -----------------------------
            # Legitimate
            # -----------------------------
            if prediction == 0:

                st.success(
                    "✅ Likely Legitimate Website"
                )

                st.markdown(
                    '<div class="safe-box">'
                    '<b>🟢 Risk Assessment</b><br>'
                    'The AI model did not detect strong '
                    'phishing indicators in this URL.'
                    '</div>',
                    unsafe_allow_html=True
                )


            # -----------------------------
            # Phishing
            # -----------------------------
            else:

                st.error(
                    "⚠️ Potential Phishing Website"
                )

                st.markdown(
                    '<div class="warning-box">'
                    '<b>🔴 Risk Assessment</b><br>'
                    'The AI model detected characteristics '
                    'that may be associated with phishing.'
                    '</div>',
                    unsafe_allow_html=True
                )


            # -----------------------------
            # Confidence
            # -----------------------------
            st.markdown("### 🤖 AI Confidence")

            st.progress(
                min(max(confidence / 100, 0.0), 1.0)
            )

            st.metric(
                "Prediction Confidence",
                f"{confidence:.2f}%"
            )


            # -----------------------------
            # Technical Information
            # -----------------------------
            with st.expander("📊 Technical Information"):

                st.write(
                    f"**Analyzed URL:** {clean_url}"
                )

                st.write(
                    f"**Prediction:** {prediction}"
                )

                st.write(
                    "**0 = Likely Legitimate**"
                )

                st.write(
                    "**1 = Potential Phishing**"
                )

                st.write(
                    f"**Confidence:** {confidence:.2f}%"
                )


            st.success(
                "✅ Detection saved to history."
            )


        except Exception as e:

            st.error(
                "❌ Unable to analyze this URL."
            )

            st.exception(e)


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "🛡️ AI-Powered Phishing Detection Platform • "
    "AI-based risk assessment"
)