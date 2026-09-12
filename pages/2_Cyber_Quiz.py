import streamlit as st

from utils.theme import apply_theme

apply_theme()

# your existing code continues here...

st.set_page_config(
    page_title="Cyber Safety Quiz",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Cyber Safety Quiz")
st.write("Test your knowledge about phishing, passwords, and online safety.")

questions = [
    {
        "question": "What is phishing?",
        "options": [
            "A type of computer hardware",
            "A cyber attack that tries to trick users into revealing information",
            "A programming language",
            "A type of antivirus"
        ],
        "answer": "A cyber attack that tries to trick users into revealing information"
    },
    {
        "question": "Which URL is generally safer?",
        "options": [
            "http://bank-example.com",
            "https://bank-example.com",
            "bank-example.free-login.com",
            "bank-login.xyz"
        ],
        "answer": "https://bank-example.com"
    },
    {
        "question": "What should you do if you receive a suspicious email link?",
        "options": [
            "Click it immediately",
            "Share it with friends",
            "Verify the sender and link before opening",
            "Reply with your password"
        ],
        "answer": "Verify the sender and link before opening"
    },
    {
        "question": "Which is the strongest password?",
        "options": [
            "password123",
            "12345678",
            "MyName2005",
            "A long unique password with mixed characters"
        ],
        "answer": "A long unique password with mixed characters"
    },
    {
        "question": "What does MFA provide?",
        "options": [
            "An additional layer of account security",
            "Faster internet",
            "More storage",
            "A new email address"
        ],
        "answer": "An additional layer of account security"
    },
    {
        "question": "What should you do if a website asks for sensitive information unexpectedly?",
        "options": [
            "Enter everything",
            "Ignore security warnings",
            "Stop and verify the website",
            "Send your password through email"
        ],
        "answer": "Stop and verify the website"
    },
    {
        "question": "Which of these can be a phishing warning sign?",
        "options": [
            "Unexpected urgent messages",
            "Suspicious URLs",
            "Requests for passwords",
            "All of the above"
        ],
        "answer": "All of the above"
    },
    {
        "question": "Why should software be updated regularly?",
        "options": [
            "To fix security vulnerabilities",
            "To make the computer heavier",
            "To remove the internet",
            "There is no reason"
        ],
        "answer": "To fix security vulnerabilities"
    },
    {
        "question": "Should you share an OTP with someone who calls you?",
        "options": [
            "Yes",
            "Only if they say they are from a bank",
            "No",
            "Only at night"
        ],
        "answer": "No"
    },
    {
        "question": "What is the purpose of an antivirus/security tool?",
        "options": [
            "To help detect and protect against malicious software",
            "To increase screen brightness",
            "To create social media accounts",
            "To replace the keyboard"
        ],
        "answer": "To help detect and protect against malicious software"
    }
]


if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


with st.form("cyber_quiz"):

    user_answers = []

    for i, q in enumerate(questions):

        st.subheader(f"Question {i + 1}")

        answer = st.radio(
            q["question"],
            q["options"],
            key=f"question_{i}"
        )

        user_answers.append(answer)

    submitted = st.form_submit_button(
        "📊 Submit Quiz",
        use_container_width=True
    )


if submitted:

    score = 0

    for i, q in enumerate(questions):

        if user_answers[i] == q["answer"]:
            score += 1

    st.session_state.quiz_submitted = True

    st.divider()

    st.subheader("🏆 Quiz Result")

    percentage = (score / len(questions)) * 100

    st.metric(
        "Your Score",
        f"{score}/{len(questions)}"
    )

    st.progress(percentage / 100)

    if percentage >= 80:
        st.success("🎉 Excellent! You have strong cyber safety awareness.")

    elif percentage >= 50:
        st.warning("👍 Good attempt! Keep learning about cyber safety.")

    else:
        st.error("📚 You should learn more about basic cyber safety practices.")


st.divider()

st.caption(
    "🛡️ AI-Powered Phishing Detection Platform | Cyber Safety Quiz"
)