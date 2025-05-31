import streamlit as st
from auth import login, initialize_session_state

initialize_session_state()
st.set_page_config(page_title="Login", layout="centered")

# Styling for the box
st.markdown("""
    <style>
    .login-box {
       
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 400px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='login-box'>", unsafe_allow_html=True)

st.subheader("🔐 Login")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

    if submit:
        success, message = login(username, password)
        if success:
            st.success(message)
            st.switch_page("pages/Home.py")
        else:
            st.error(message)

st.markdown("</div>", unsafe_allow_html=True)
st.page_link("pages/z_Signup.py", label="👉  Don't have an account? Sign up here")
