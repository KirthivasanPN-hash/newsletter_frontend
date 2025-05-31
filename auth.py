# auth.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL", "https://newsletter-app-ce6e.onrender.com")

def initialize_session_state():
    if "user" not in st.session_state:
        st.session_state.user = None
    if "signup_success" not in st.session_state:
        st.session_state.signup_success = False

def signup(username, password, role):
    if not username or not password:
        return False, "Username and password are required"
    
    try:
        response = requests.post(
            f"{API_URL}/users/",
            json={"username": username, "password": password, "role": role}
        )
        if response.status_code == 200:
            st.session_state.signup_success = True
            return True, "User created successfully! Please sign in."
        return False, response.json().get("detail", "Signup failed.")
    except requests.exceptions.ConnectionError:
        return False, "Server not reachable. Is the backend running?"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def login(username, password):
    if not username or not password:
        return False, "Username and password are required"
    
    try:
        response = requests.post(
            f"{API_URL}/login/",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.user = {
                "username": data["username"],
                "role": data["role"]
            }
            return True, f"Welcome {data['username']}!"
        return False, response.json().get("detail", "Invalid credentials")
    except requests.exceptions.ConnectionError:
        return False, "Server not reachable. Is the backend running?"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def logout():
    st.session_state.user = None
    st.session_state.signup_success = False

def get_user_role():
    return st.session_state.user["role"] if st.session_state.user else None
