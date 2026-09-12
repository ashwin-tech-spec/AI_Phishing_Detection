import streamlit as st

from utils.clone_website_detector import predict_clone_website
from utils.database import save_detection

st.set_page_config(
    page_title="Clone Website Detection",
    page_icon="🌐",
    layout="wide"
)

# ============================================================
# CUSTOM CSS + ANIMATIONS
# ============================================================

st.markdown("""
<style>

/* ==============================
   MAIN ANIMATED BACKGROUND
   ============================== */

.stApp {
    background:
        radial-gradient(circle at 10% 20%, rgba(0, 153, 255, 0.22), transparent 25%),
        radial-gradient(circle at 90% 15%, rgba(168, 85, 247, 0.25), transparent 25%),
        radial-gradient(circle at 80% 85%, rgba(16, 185, 129, 0.20), transparent 25%),
        linear-gradient(
            135deg,
            #e8f1ff,
            #f7efff,
            #eafcff,
            #effff7
        );

    background-size: 400% 400%;

    animation: backgroundMove 15s ease infinite;
}


/* Moving gradient */

@keyframes backgroundMove {

    0% {
        background-position: 0% 50%;
    }

    25% {
        background-position: 50% 100%;
    }

    50% {
        background-position: 100% 50%;
    }

    75% {
        background-position: 50% 0%;
    }

    100% {
        background-position: 0% 50%;
    }

}


/* ==============================
   MAIN CONTENT
   ============================== */

.block-container {

    padding-top: 2rem;
    padding-bottom: 4rem;

}


/* ==============================
   HEADER
   ============================== */

.clone-header {

    font-size: 44px;
    font-weight: 800;

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed,
        #0891b2
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;

    animation: titleGlow 3s ease-in-out infinite;

}


@keyframes titleGlow {

    0% {
        filter: brightness(1);
    }

    50% {
        filter: brightness(1.3);
    }

    100% {
        filter: brightness(1);
    }

}


.clone-subtitle {

    font-size: 18px;

    color: #475569;

    margin-bottom: 25px;

}


/* ==============================
   GLASS CARDS
   ============================== */

.input-card {

    padding: 30px;

    border-radius: 22px;

    background: rgba(255,255,255,0.72);

    backdrop-filter: blur(15px);

    border: 1px solid rgba(255,255,255,0.7);

    box-shadow:
        0 15px 40px rgba(37,99,235,0.12);

    margin-top: 20px;

    transition: all 0.3s ease;

}


.input-card:hover {

    transform: translateY(-5px);

    box-shadow:
        0 20px 50px rgba(124,58,237,0.18);

}


/* ==============================
   RESULT CARD
   ============================== */

.result-card {

    padding: 28px;

    border-radius: 22px;

    background: rgba(255,255,255,0.78);

    backdrop-filter: blur(15px);

    border: 1px solid rgba(255,255,255,0.7);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.08);

    margin-top: 20px;

    animation: resultAppear 0.7s ease;

}


@keyframes resultAppear {

    from {

        opacity: 0;

        transform: translateY(20px);

    }

    to {

        opacity: 1;

        transform: translateY(0);

    }

}


/* ==============================
   INFORMATION CARD
   ============================== */

.info-card {

    padding: 22px;

    border-radius: 18px;

    background: rgba(255,255,255,0.70);

    backdrop-filter: blur(12px);

    border-left: 5px solid #7c3aed;

    box-shadow:
        0 10px 30px rgba(124,58,237,0.10);

    margin-top: 20px;

}


/* ==============================
   BUTTON
   ============================== */

.stButton > button {

    height: 55px;

    border-radius: 14px;

    border: none;

    font-size: 17px;

    font-weight: 700;

    color: white;

    background:
        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed,
            #0891b2
        );

    background-size: 200% auto;

    box-shadow:
        0 8px 25px rgba(37,99,235,0.25);

    transition: all 0.3s ease;

}


.stButton > button:hover {

    background-position: right center;

    transform: translateY(-3px);

    box-shadow:
        0 12px 30px rgba(124,58,237,0.35);

}


/* ==============================
   TEXT INPUT
   ============================== */

.stTextInput input {

    border-radius: 12px;

    border: 2px solid #dbeafe;

    background: rgba(255,255,255,0.85);

    padding: 15px;

    font-size: 16px;

    transition: all 0.3s ease;

}


.stTextInput input:focus {

    border-color: #7c3aed;

    box-shadow:
        0 0 0 4px rgba(124,58,237,0.12);

}


/* ==============================
   SECTION HEADINGS
   ============================== */

h1, h2, h3 {

    color: #172554;

}


/* ==============================
   SECURITY NOTICE
   ============================== */

.security-box {

    padding: 18px;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            rgba(219,234,254,0.85),
            rgba(224,231,255,0.85)
        );

    border: 1px solid #bfdbfe;

    box-shadow:
        0 8px 25px rgba(37,99,235,0.08);

}


/* ==============================
   FLOATING DECORATION
   ============================== */

.floating-circle {

    position: fixed;

    border-radius: 50%;

    pointer-events: none;

    z-index: 0;

}


.circle-one {

    width: 120px;

    height: 120px;

    background: rgba(59,130,246,0.15);

    top: 15%;

    left: 5%;

    animation: floatOne 8s ease-in-out infinite;

}


.circle-two {

    width: 160px;

    height: 160px;

    background: rgba(168,85,247,0.13);

    right: 5%;

    top: 45%;

    animation: floatTwo 10s ease-in-out infinite;

}


.circle-three {

    width: 100px;

    height: 100px;

    background: rgba(16,185,129,0.13);

    bottom: 10%;

    left: 35%;

    animation: floatThree 7s ease-in-out infinite;

}


@keyframes floatOne {

    0%,100% {

        transform: translate(0,0);

    }

    50% {

        transform: translate(30px,40px);

    }

}


@keyframes floatTwo {

    0%,100% {

        transform: translate(0,0);

    }

    50% {

        transform: translate(-40px,30px);

    }

}


@keyframes floatThree {

    0%,100% {

        transform: translate(0,0);

    }

    50% {

        transform: translate(20px,-30px);

    }

}


/* ==============================
   FOOTER
   ============================== */

.footer-text {

    text-align: center;

    color: #64748b;

    font-size: 14px;

    margin-top: 35px;

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FLOATING BACKGROUND ELEMENTS
# ============================================================

st.markdown("""
<div class="floating-circle circle-one"></div>
<div class="floating-circle circle-two"></div>
<div class="floating-circle circle-three"></div>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="clone-header">🌐 Clone Website Detection</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="clone-subtitle">'
    'AI-powered analysis for detecting potential phishing '
    'and website impersonation characteristics.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SECURITY NOTICE
# ============================================================

st.markdown("""
<div class="security-box">

🛡️ <b>Security Notice</b><br>

Enter only the website URL. Do not enter passwords,
OTP codes, banking PINs, or other sensitive information.

</div>
""", unsafe_allow_html=True)


# ============================================================
# URL INPUT
# ============================================================

st.markdown(
    '<div class="input-card">',
    unsafe_allow_html=True
)

st.markdown("### 🔗 Website Analysis")

st.write(
    "Enter the URL you want the AI model to analyze."
)

url = st.text_input(
    "Website URL",
    placeholder="https://example.com",
    label_visibility="collapsed"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

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

        if not clean_url.lower().startswith(
            ("http://", "https://")
        ):

            clean_url = "https://" + clean_url

        try:

            # Loading animation

            with st.spinner(
                "🤖 AI is analyzing the website..."
            ):

                result = predict_clone_website(
                    clean_url
                )


            # =================================================
            # RESULT
            # =================================================

            st.divider()

            st.subheader(
                "🔎 Detection Result"
            )

            prediction = result["prediction"]

            confidence = result["confidence"]

            # =================================================
            # SAVE TO HISTORY
            # =================================================

            save_detection(
                url=clean_url,
                prediction=prediction,
                confidence=confidence,
                detection_type="Clone Website Detection"
            )


            # =================================================
            # LEGITIMATE
            # =================================================

            if prediction == 0:

                st.success(
                    "🟢 Website appears legitimate"
                )

                st.markdown("""
                <div class="result-card">

                <h3>🟢 Low Clone / Phishing Risk</h3>

                <p>
                The AI model did not detect strong
                indicators associated with a phishing
                or impersonation website.
                </p>

                </div>
                """, unsafe_allow_html=True)


            # =================================================
            # PHISHING / CLONE
            # =================================================

            else:

                st.error(
                    "🚨 Potential Clone / Brand Impersonation Detected"
                )

                st.markdown("""
                <div class="result-card">

                <h3>🚨 Clone / Brand Impersonation Risk</h3>

                <p>
                The AI model detected characteristics
                that may be associated with a phishing
                or brand impersonation website.
                </p>

                </div>
                """, unsafe_allow_html=True)


            # =================================================
            # CONFIDENCE
            # =================================================

            st.markdown(
                "### 🤖 AI Confidence"
            )

            st.progress(
                min(
                    max(
                        confidence / 100,
                        0.0
                    ),
                    1.0
                )
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )

            with col2:

                if prediction == 0:

                    st.metric(
                        "Risk Level",
                        "Low"
                    )

                else:

                    st.metric(
                        "Risk Level",
                        "High"
                    )

            with col3:

                if prediction == 0:

                    st.metric(
                        "Status",
                        "Legitimate"
                    )

                else:

                    st.metric(
                        "Status",
                        "Suspicious"
                    )


            # =================================================
            # BRAND INFORMATION
            # =================================================

            detected_brand = result.get(
                "detected_brand"
            )

            legitimate_website = result.get(
                "legitimate_website"
            )


            if detected_brand:

                st.markdown("""
                <div class="info-card">

                <h3>🏷️ Brand Reference</h3>

                </div>
                """, unsafe_allow_html=True)

                st.write(
                    f"**Detected Brand:** "
                    f"{detected_brand}"
                )

                if legitimate_website:

                    st.write(
                        f"**Reference Website:** "
                        f"{legitimate_website}"
                    )


            # =================================================
            # TECHNICAL INFORMATION
            # =================================================

            with st.expander(
                "📊 View Technical Information"
            ):

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
                    "**1 = Potential Phishing / Clone / Brand Impersonation**"
                )

                st.write(
                    f"**AI Confidence:** "
                    f"{confidence:.2f}%"
                )


        except Exception as e:

            st.error(
                "❌ Unable to analyze this website."
            )

            st.exception(e)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown("""
<div class="footer-text">

🛡️ <b>AI-Powered Phishing Detection Platform</b><br>

Clone Website Detection • Cyber Safety • AI Security

</div>
""", unsafe_allow_html=True)