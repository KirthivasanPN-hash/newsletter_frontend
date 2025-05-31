import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from time import sleep
import json
from auth import logout

st.set_page_config(
    page_title="Newsletter Management",
    page_icon="📰",
    layout="wide"
)

# Custom CSS for better card styling
st.markdown("""
    <style>
    .newsletter-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #1a237e;  
        transition: all 0.3s ease;  /* Smooth transition for hover effect */
        display: flex;
        flex-direction: column;
    }
    .newsletter-card:hover {
        box-shadow: 0 6px 12px rgba(26, 35, 126, 0.2);  /* Enhanced shadow on hover */
        transform: translateY(-2px);  /* Slight lift effect on hover */
    }
    .newsletter-image {
        width: 100%;
        margin-bottom: 15px;
    }
    .newsletter-image img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
    }
    .newsletter-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        color: #1a237e;  
    }
    .newsletter-content {
        font-size: 16px;
        color: #333; 
        margin-bottom: 15px;
        flex-grow: 1;  
    }
    .newsletter-status {
        font-size: 14px;
        color: #666;  
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📰 Newsletter Management")




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
    if st.sidebar.button("🚪 Logout"):
        logout()
        st.success("Logged out successfully!")
        sleep(0.5)
        st.switch_page("pages/z_Login.py")

make_sidebar()

# Function to fetch newsletters from the backend
def fetch_newsletters():
    try:
        response = requests.get("https://newsletter-app-ce6e.onrender.com/newsletters/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch newsletters")
            return []
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        return []

# Function to delete a newsletter
# def delete_newsletter(newsletter_id):
#     try:
#         response = requests.delete(f"https://newsletter-app-ce6e.onrender.com/newsletters/{newsletter_id}")
#         if response.status_code == 200:
#             st.success("Newsletter deleted successfully!")
#             st.rerun()
#         else:
#             st.error("Failed to delete newsletter")
#     except Exception as e:
#         st.error(f"Error deleting newsletter: {str(e)}")

# # Function to edit a newsletter
# def edit_newsletter(newsletter):
#     st.session_state.newsletter_data = {
#         'title': newsletter['title'],
#         'content': newsletter['content'],
#         'status': newsletter['status'],
#         'image': None
#     }
#     st.session_state.newsletter_id = newsletter['id']
#     st.switch_page("pages/Newsletter_Form.py")

# Function to display a newsletter card
def display_newsletter_card(newsletter):
    with st.container():
        st.markdown(f"""
            <div class="newsletter-card">
                <div class="newsletter-image">
                    {f'<img src="https://newsletter-app-ce6e.onrender.com/newsletters/{newsletter["id"]}/image" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px; margin-bottom: 15px;">' if newsletter.get('image_url') else ''}
                </div>
                <div class="newsletter-title">{newsletter['title']}</div>
                <div class="newsletter-status">Status: {newsletter['status']}</div>
                <div class="newsletter-content">{newsletter['content'][:200]}...</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Read more button
        if st.button(f"Read More", key=f"read_more_{newsletter['id']}"):
            st.session_state['selected_newsletter'] = newsletter
            st.switch_page("pages/Newsletter_Detail.py")


# Main content
newsletters = [n for n in fetch_newsletters() if n['status'].lower() != 'draft']

if newsletters:
    # Create columns for the grid layout
    cols = st.columns(3)
    # Display newsletters in a grid
    for idx, newsletter in enumerate(newsletters):
        with cols[idx % 3]:
            display_newsletter_card(newsletter)
else:
    st.info("No newsletters available.")
