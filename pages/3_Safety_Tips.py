import streamlit as st

from utils.theme import apply_theme

apply_theme()

# your existing code continues here...

st.set_page_config(
    page_title="Cyber Safety Tips",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ Cyber Safety Tips")

st.write(
    "Follow these simple practices to protect yourself from phishing "
    "and other common online threats."
)


st.header("🔗 1. Check Website URLs")

st.write("""
Before entering sensitive information:

- Check the website address carefully.
- Look for spelling mistakes in the domain.
- Be careful with unfamiliar domains.
- HTTPS is useful, but HTTPS alone does not guarantee that a website is legitimate.
- Avoid clicking suspicious links from unknown sources.
""")


st.header("🔐 2. Protect Your Passwords")

st.write("""
- Use a different password for important accounts.
- Use long, unique passwords.
- Never share your password with others.
- Avoid using easily guessed information.
- Consider using a trusted password manager.
""")


st.header("📱 3. Protect OTPs and Verification Codes")

st.write("""
- Never share OTPs with other people.
- Banks and legitimate services generally do not need you to tell them your OTP.
- Be suspicious of unexpected calls asking for verification codes.
""")


st.header("📧 4. Be Careful With Emails")

st.write("""
Watch for:

- Unexpected messages
- Urgent requests
- Suspicious attachments
- Unknown senders
- Requests for passwords or financial information
- Links that don't match the claimed website
""")


st.header("💳 5. Protect Financial Information")

st.write("""
- Don't enter banking information on suspicious websites.
- Verify the website before making payments.
- Don't share card PINs, passwords, or OTPs.
- Avoid making sensitive transactions on untrusted devices.
""")


st.header("🔄 6. Keep Software Updated")

st.write("""
Regular updates can fix security vulnerabilities.

Keep your:

- Operating system
- Browser
- Applications
- Security software

updated whenever possible.
""")


st.header("📲 7. Be Careful With Apps")

st.write("""
- Install apps from trusted sources.
- Check the developer/publisher.
- Review requested permissions.
- Avoid suspicious APK files and unknown applications.
""")


st.header("🚨 8. If You Think You Encountered Phishing")

st.write("""
1. Don't enter any more information.
2. Close the suspicious page.
3. If you entered a password, change it from the legitimate website.
4. Enable multi-factor authentication where available.
5. Monitor important accounts for unusual activity.
6. Report the suspicious message or website through the appropriate service.
""")


st.success(
    "🛡️ Remember: Think before you click, verify before you trust."
)

st.divider()

st.caption(
    "🛡️ AI-Powered Phishing Detection Platform | Cyber Safety"
)