import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>

        /* Main application background */
        .stApp {
            background-color: #0b1220;
        }

        /* Main content area */
        .main {
            background-color: #0b1220;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #111827;
        }

        /* Text */
        .stApp,
        .stApp p,
        .stApp label,
        .stApp span {
            color: #f3f4f6;
        }

        /* Headings */
        h1, h2, h3 {
            color: #ffffff !important;
        }

        /* Cards */
        .custom-card {
            background-color: #111827;
            border: 1px solid #263244;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }

        /* Buttons */
        .stButton > button {
            border-radius: 10px;
            font-weight: 600;
        }

        /* Input boxes */
        .stTextInput input,
        .stTextArea textarea {
            background-color: #111827;
            color: #ffffff;
            border: 1px solid #374151;
            border-radius: 10px;
        }

        /* Select boxes */
        div[data-baseweb="select"] > div {
            background-color: #111827;
            color: #ffffff;
        }

        /* Remove extra top spacing */
        .block-container {
            padding-top: 2rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )