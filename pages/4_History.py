import streamlit as st

from utils.theme import apply_theme

apply_theme()

# your existing code continues here...
from utils.database import get_history, clear_history

st.set_page_config(
    page_title="Detection History",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Detection History")

st.write(
    "View all URLs analyzed by the AI-Powered Phishing Detection Platform."
)

# Get history from SQLite database
history = get_history()


# -----------------------------
# No history
# -----------------------------

if len(history) == 0:

    st.info(
        "No detection history yet. Analyze a URL from the detection pages."
    )


# -----------------------------
# Display history
# -----------------------------

else:

    st.subheader("🔎 Previous Detection Results")

    for i, item in enumerate(history):

        # Database columns:
        # id, url, prediction, confidence, detection_type, checked_at

        detection_id = item[0]
        url = item[1]
        prediction = item[2]
        confidence = item[3]
        detection_type = item[4]
        checked_at = item[5]

        with st.container():

            st.write(f"### Detection #{detection_id}")

            st.write(f"**URL:** {url}")

            # Detection type
            if detection_type == "Clone Website Detection":

                st.info(
                    f"🌐 **Detection Type:** {detection_type}"
                )

            else:

                st.info(
                    f"🔗 **Detection Type:** {detection_type}"
                )

            # Prediction result
            if prediction == 0:

                st.success(
                    f"✅ Likely Legitimate — "
                    f"{confidence:.2f}% confidence"
                )

            else:

                st.error(
                    f"⚠️ Potential Phishing / Clone Website — "
                    f"{confidence:.2f}% confidence"
                )

            # Date and time
            st.caption(
                f"🕒 Checked: {checked_at}"
            )

            st.divider()


    # -----------------------------
    # Clear History
    # -----------------------------

    if st.button(
        "🗑️ Clear History",
        use_container_width=True
    ):

        clear_history()

        st.success("Detection history cleared successfully.")

        st.rerun()


st.caption(
    "🛡️ AI-Powered Phishing Detection Platform | Detection History"
)