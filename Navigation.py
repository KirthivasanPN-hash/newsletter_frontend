# navigation.py

import streamlit as st
from time import sleep
from auth import initialize_session_state, logout

# Initialize session variables
initialize_session_state()

if not st.session_state.get("user"):
    st.switch_page("pages/z_Login.py")  # redirect to login if not authenticated

role = st.session_state.user["role"]

# Sidebar rendering
st.sidebar.title("📬 Newsletter App")
st.sidebar.page_link("pages/Home.py", label="🏠 Home")
st.sidebar.page_link("pages/Newsletter_Detail.py", label="📰 Newsletter Detail")

if role == "admin":
    st.sidebar.page_link("pages/Manage_newsletters.py", label="🛠️ Manage Newsletters")
    st.sidebar.page_link("pages/Newsletter_Form.py", label="✏️ Create/Edit Newsletter")

st.sidebar.markdown("---")

# Logout button
if st.sidebar.button("🚪 Logout"):
    logout()
    st.success("Logged out successfully!")
    sleep(0.5)
    st.switch_page("pages/z_Login.py")  
