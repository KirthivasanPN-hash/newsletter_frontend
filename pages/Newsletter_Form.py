import streamlit as st
import requests
from PIL import Image
import io

# Configure the page
st.set_page_config(
    page_title="Newsletter Form",
    page_icon="📝",
    layout="wide"
)


if "user" not in st.session_state or st.session_state["user"]["role"] != "admin":
    st.warning("You must be an admin to access this page.")
    st.stop()

# Title
st.title("📝 Newsletter Form")

# Initialize session state for newsletter data if not exists
if 'newsletter_data' not in st.session_state:
    st.session_state.newsletter_data = {
        'title': '',
        'content': '',
        'status': 'draft',
        'image': None
    }


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

    
    
        
make_sidebar()


# Form for newsletter creation/editing
with st.form("newsletter_form"):
    title = st.text_input("Title", value=st.session_state.newsletter_data['title'])
    content = st.text_area("Content", value=st.session_state.newsletter_data['content'], height=300)
    status = st.selectbox(
        "Status",
        ["draft", "published"],
        index=0 if st.session_state.newsletter_data['status'] == 'draft' else 1
    )
    image = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])

    submit_button = st.form_submit_button("Save Newsletter")

    if submit_button:
        if not title or not content:
            st.error("Please fill in all required fields")
        else:
            try:
                data = {
                    'title': title,
                    'content': content,
                    'status': status
                }
                files = {}
                if image is not None: 
                    files['image'] = (image.name, image, image.type)

                if 'newsletter_id' in st.session_state:
                    # Update
                    response = requests.put(
                        f"https://newsletter-app-ce6e.onrender.com/newsletters/{st.session_state.newsletter_id}/with-image/",
                        data=data,
                        files=files if files else None
                    )
                else:
                    # Create
                    response = requests.post(
                        "https://newsletter-app-ce6e.onrender.com/newsletters/with-image/",
                        data=data,
                        files=files if files else None
                    )

                if response.status_code in (200, 201):
                    st.success("Newsletter saved successfully!")
                else:
                    st.error(f"Failed to save newsletter: {response.text}")
                    st.stop()

                # Clear session state
                st.session_state.newsletter_data = {
                    'title': '',
                    'content': '',
                    'status': 'draft',
                    'image': None
                }
                if 'newsletter_id' in st.session_state:
                    del st.session_state.newsletter_id

                st.switch_page("pages/Home.py")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
