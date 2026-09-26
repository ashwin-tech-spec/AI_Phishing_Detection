import streamlit as st
from utils.clone_website_detector import predict_clone_website
from utils.database import save_detection


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Clone Website Detection",
    page_icon="🌐",
    layout="wide"
)


# =========================================================
# PAGE TITLE
# =========================================================

st.title("🌐 Clone Website Detection")

st.subheader(
    "AI-powered detection of potential phishing and "
    "website impersonation characteristics."
)

st.write(
    "Enter a website URL and our trained Machine Learning "
    "model will analyze website-related characteristics."
)


# =========================================================
# SECURITY NOTICE
# =========================================================

st.info(
    "🛡️ Security Notice: Enter only the website URL. "
    "Do not enter passwords, OTPs, PINs, or other sensitive information."
)


# =========================================================
# URL INPUT
# =========================================================

st.markdown("---")

st.header("🔗 Enter Website URL")

url = st.text_input(
    "Website URL",
    placeholder="Example: https://example.com"
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if st.button(
    "🔍 Analyze Website",
    use_container_width=True
):

    if not url.strip():

        st.warning(
            "⚠️ Please enter a website URL."
        )

    else:

        clean_url = url.strip()

        # Add https if user did not enter protocol
        if not clean_url.lower().startswith(
            ("http://", "https://")
        ):
            clean_url = "https://" + clean_url

        try:

            # =================================================
            # MODEL PREDICTION
            # =================================================

            with st.spinner(
                "🤖 AI is analyzing the website..."
            ):

                result = predict_clone_website(
                    clean_url
                )


            prediction = result["prediction"]
            confidence = result["confidence"]


            # =================================================
            # SAVE HISTORY
            # =================================================

            save_detection(
                url=clean_url,
                prediction=prediction,
                confidence=confidence,
                detection_type="Clone Website Detection"
            )


            # =================================================
            # RESULT
            # =================================================

            st.markdown("---")

            st.header("🔎 Detection Result")


            # =================================================
            # PHISHING / CLONE
            # =================================================

            if prediction == 1:

                st.error(
                    "🚨 Potential Phishing / Clone Website"
                )

                st.metric(
                    "AI Confidence",
                    f"{confidence:.2f}%"
                )

                st.warning(
                    "The model detected characteristics "
                    "that may be associated with a phishing "
                    "or impersonation-style website."
                )


            # =================================================
            # LEGITIMATE
            # =================================================

            else:

                st.success(
                    "✅ Website Appears Safer"
                )

                st.metric(
                    "AI Confidence",
                    f"{confidence:.2f}%"
                )

                st.info(
                    "The model did not detect strong "
                    "phishing or impersonation characteristics."
                )


            # =================================================
            # WEBSITE INFORMATION
            # =================================================

            st.markdown("---")

            st.header("📊 Analysis Information")

            col1, col2 = st.columns(2)

            with col1:

                st.write("**Website URL:**")

                st.code(
                    clean_url
                )


            with col2:

                st.write("**Detection Type:**")

                st.write(
                    "Clone / Phishing Website Detection"
                )


            # =================================================
            # CONFIDENCE
            # =================================================

            st.markdown("---")

            st.subheader("📈 Model Confidence")

            st.progress(
                min(confidence / 100, 1.0)
            )

            st.write(
                f"AI Confidence: **{confidence:.2f}%**"
            )


            # =================================================
            # TECHNICAL DETAILS
            # =================================================

            st.markdown("---")

            with st.expander(
                "🔧 View Technical Details"
            ):

                st.write(
                    "The Clone Website Detection model "
                    "uses website and URL-related features "
                    "to classify potentially phishing or "
                    "legitimate websites."
                )

                st.write(
                    "**Machine Learning Model:** "
                    "Random Forest"
                )

                st.write(
                    "**Detection Type:** "
                    "Phishing / Clone Website Detection"
                )

                st.write(
                    "**Result:**",
                    prediction
                )


            # =================================================
            # SAFETY RECOMMENDATION
            # =================================================

            st.markdown("---")

            st.subheader("🛡️ Safety Recommendation")

            if prediction == 1:

                st.warning(
                    "Avoid entering passwords, OTPs, banking "
                    "information, or other sensitive information "
                    "on this website until its authenticity is verified."
                )

            else:

                st.success(
                    "The website appears safer according to "
                    "the model. However, always verify the "
                    "website address before entering sensitive information."
                )


        except Exception as e:

            st.error(
                "❌ An error occurred while analyzing the website."
            )

            st.exception(e)


# =========================================================
# INFORMATION SECTION
# =========================================================

st.markdown("---")

st.header("ℹ️ How Clone Website Detection Works")

st.write(
    """
The system analyzes website-related characteristics and
uses a trained Random Forest Machine Learning model to
identify potentially suspicious or phishing/impersonation
websites.
"""
)


# =========================================================
# IMPORTANT INFORMATION
# =========================================================

st.info(
    "⚠️ AI predictions are based on the features available "
    "to the model and should not be treated as a guarantee "
    "that a website is safe or malicious."
)