import streamlit as st
from auth import signup, initialize_session_state

# Initialize session state
initialize_session_state()

# Page settings
st.set_page_config(page_title="Sign Up", layout="centered")

# Hide default sidebar navigation
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    .signup-box {
        
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        width: 100%;
        max-width: 400px;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Only show "Sign Up" in sidebar
st.sidebar.page_link("pages/z_Signup.py", label="Sign Up")

# Sign Up form UI
st.markdown("<div class='signup-box'>", unsafe_allow_html=True)
st.subheader("📝 Create a New Account")

with st.form("signup_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])
    submit = st.form_submit_button("Create Account")

    if submit:
        success, message = signup(username, password, role)
        if success:
            st.success(message)
            st.switch_page("pages/z_Login.py")
        else:
            st.error(message)

st.markdown("</div>", unsafe_allow_html=True)
st.page_link("pages/z_Login.py", label="✅ Already have an account? Log in here")
