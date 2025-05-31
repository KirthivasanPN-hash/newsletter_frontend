import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Configure the page
st.set_page_config(
    page_title="Newsletter Detail",
    page_icon="📰",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background-color: black;
    }
    .css-1d391kg {
        background-color: #1a237e;
    }
    .css-1d391kg .css-1v0mbdj {
        color: white;
    }
    .newsletter-detail {
        background-color: black;
        border-radius: 5px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .newsletter-title {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        color: white;
    }
    .newsletter-content {
        font-size: 18px;
        line-height: 1.6;
        color: #e0e0e0;  /* Light gray for better readability on dark background */
        margin-bottom: 20px;
    }
    .newsletter-meta {
        font-size: 14px;
        color: #bdbdbd;  /* Lighter gray for meta information */
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


def make_sidebar():
    if not st.session_state.get("user"):
        st.switch_page("pages/z_Login.py")

    role = st.session_state.user["role"]

    st.sidebar.title("📬 Newsletter App")
    st.sidebar.page_link("pages/Home.py", label="🏠 Home")
    st.sidebar.page_link("pages/Newsletter_Detail.py", label="📰 Newsletter Detail")

    if role == "admin":
        st.sidebar.page_link("pages/Manage_newsletters.py", label="🛠️ Manage Newsletters")
        st.sidebar.page_link("pages/Newsletter_Form.py", label="✏️ Create/Edit Newsletter")

    st.sidebar.markdown("---")
    
        
make_sidebar()


if st.button("← Back to Home"):
    st.switch_page("Home.py")

# Get the selected newsletter from session state
if 'selected_newsletter' not in st.session_state:
    st.error("No newsletter selected")
    st.stop()

newsletter = st.session_state['selected_newsletter']

# Display newsletter details
st.markdown(f"""
    <div class="newsletter-detail">
        <div class="newsletter-title">{newsletter['title']}</div>
        <div class="newsletter-meta">
            Status: {newsletter['status']}<br>
            Created: {newsletter['created_at']}<br>
            Last Updated: {newsletter['updated_at']}
        </div>
    </div>
""", unsafe_allow_html=True)

# Display image if available
if newsletter.get('image_url'):
    try:
        response = requests.get(f"https://newsletter-app-ce6e.onrender.com/newsletters/{newsletter['id']}/image")
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            st.image(image, width=600)
    except Exception as e:
        st.warning(f"Could not load image: {str(e)}")

# Display full content
st.markdown(f"""
    <div class="newsletter-content">
        {newsletter['content']}
    </div>
""", unsafe_allow_html=True) 