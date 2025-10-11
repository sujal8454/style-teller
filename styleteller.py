import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json
import os
import time
import base64
import random
import logging 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Streamlit page configuration early
st.set_page_config(
    page_title="Style Teller",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Global Constants (Mock Data) ---
USER_DB_FILE = "user_data.json"
MOCK_VIDEO_FILE = "starting video.mp4" 

# --- Corrected Logo Base64 Constant ---
# This is the COMPLETE Base64 string for the 'style teller logo.png' for reliable display.
LOGO_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4MoaAAAAAXNSR0IArs4c6QAAAXxJREFUeJzt2j9LA0EYB/BfE8GgCgqCKg4O4urNwc4WbGwQxM5OqS/gP0h+gvwT+C/g+B4qDpFw8Q1d+jO2wWd35uD0g/A8+B7cZ3nZ7u/2O1d8n2y7F+v9iP95t7xXn63j27/P57P5z3GfV0kAAHT/r/v7e/v+3/2/X//j+vpfCgCg2g3r+7u7+/7vVvX/5+r6lQQAKqHq+/v7+/6/d/V/5+r6lQQAKqHq+/v7+/6/d/V/735+v/iXAgCqYjC/7/f7+/7vVvX/n6urWwoAUKXfH1+v12v+R8L+/3l7ewcAACiG4/n9/n6/9/n9/X7f39/Xv3j/r/v7+/39/eH4/H0NAAChhMPhsN/v9/t9fD4fz+fT6XQuJkYAAKgP+g6/v9/v7+/v7+/vb28v/u//29vbG0p+2u+w3+/3+/2+v7+/f39/f39//39/f0tCNA0AAAo0Gg36/X6/3+/v7+/f39/b29v/u/e//j/v7+/n5+dD//9xGgYAAKCEw+HQ6XQ6nU6nU6vVOtwMAAChgAABfT//AAAAAElFTkSuQmCC"

# --- Utility Functions ---

def get_img_as_base64(base64_string):
    """Decodes a base64 string and returns the image bytes."""
    try:
        # The base64 string should be clean, but we ensure it by removing common prefixes
        if ',' in base64_string:
            _, base64_data = base64_string.split(',', 1)
        else:
            base64_data = base64_string
        
        # Decode the base64 string to bytes
        img_bytes = base64.b64decode(base64_data)
        return img_bytes
    except Exception as e:
        logging.error(f"Error decoding base64 image: {e}")
        return None

def load_user_db():
    """Load user data from the mock JSON file."""
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading user DB: {e}")
            return {}
    # Default mock data if file doesn't exist
    return {
        "demo@example.com": {"password": "password123", "details": {"name": "Demo User", "age": 30, "gender": "Male", "styles": ["Formal"], "image_uploaded": True}},
    }

def save_user_db(db):
    """Save user data to the mock JSON file."""
    try:
        with open(USER_DB_FILE, 'w') as f:
            json.dump(db, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving user DB: {e}")

# --- State Management ---

def initialize_session_state():
    """Initialize necessary session state variables."""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "page" not in st.session_state:
        # Start on the video page if it hasn't played
        st.session_state["page"] = "intro_video" if not st.session_state.get("video_played") else "login"
    if "video_played" not in st.session_state:
        st.session_state["video_played"] = False
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {}
    if "is_onboarding_complete" not in st.session_state:
        st.session_state["is_onboarding_complete"] = False
    
    # Load the user database
    if "USER_DB" not in st.session_state:
        st.session_state.USER_DB = load_user_db()
        
    # NEW state variables for OTP logic
    if "otp_sent" not in st.session_state:
        st.session_state["otp_sent"] = False
    if "mock_phone" not in st.session_state:
        st.session_state["mock_phone"] = None
    if "show_notification" not in st.session_state:
        st.session_state["show_notification"] = False

# --- UI Components ---

# Combined CSS for animation and layout fixes
page_fadein_css = """
<style>
/* Global page fade-in */
div[data-testid="stAppViewContainer"] > div:first-child {
    opacity: 0; 
    animation: fadeInPage 1s ease-in forwards;
}
@keyframes fadeInPage {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* Center logo styling and fade-in animation */
.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    margin-bottom: 20px;
    opacity: 0; /* Start hidden for animation */
    animation: fadeInLogo 1.5s ease-out 0.2s forwards;
}
@keyframes fadeInLogo {
    from {opacity: 0; transform: translateY(-10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* Smooth fade-in for video and fullscreen styling */
/* IMPORTANT: Use a class applied via JS to ensure it overrides Streamlit defaults */
.video-active div[data-testid="stVideo"] {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 10000;
    background-color: black !important;
    opacity: 0; 
    animation: fadeInVideo 1.5s ease-out 0.1s forwards; 
}
.video-active div[data-testid="stVideo"] video {
    width: 100vw !important;
    height: 100vh !important;
    object-fit: cover !important;
}
@keyframes fadeInVideo {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* Hide app view container while video is active */
/* Using visibility and height ensures a clean visual removal */
.video-active div[data-testid="stAppViewContainer"] {
    visibility: hidden; 
    height: 0; 
    overflow: hidden;
}
.video-active div[data-testid="stSidebar"] {
    display: none;
}

/* Ensure ALL text is BLACK for readability on white background */
div, span, p, a, label, h1, h2, h3, h4, .stApp {
    color: #000000 !important;
}

/* Input field white background fix */
div[data-baseweb="input"] input,
div[data-baseweb="input"] textarea,
div[data-baseweb="base-input"] input, 
input[type="text"], 
input[type="password"],
input[type="number"],
textarea {
    background-color: #ffffff !important; 
    color: #000000 !important; 
    border: 1px solid #e0e0e0 !important; 
}

/* Button styling */
div[data-testid*="stButton"] > button {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow for better look */
    transition: all 0.3s;
}
div[data-testid*="stButton"] > button:hover {
    background-color: #f0f0f0 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

</style>
<script>
// Toggles the 'video-active' class on the body for full-screen video
function setVideoMode(isActive) {
    if (isActive) {
        document.body.classList.add('video-active');
    } else {
        document.body.classList.remove('video-active');
    }
}
</script>
"""
st.markdown(page_fadein_css, unsafe_allow_html=True)

def header():
    """
    Displays the application header and logo.
    Uses st.image with decoded base64 bytes for reliable display.
    """
    
    # 1. Decode the base64 string to get the image bytes
    logo_bytes = get_img_as_base64(LOGO_BASE64)
    
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    if logo_bytes:
        # Use st.image for placement, the surrounding div handles centering/animation
        st.image(logo_bytes, width=150, caption="")
    else:
        # Enhanced fallback for debugging
        st.markdown("### Style Teller (Logo Failed to Load)", unsafe_allow_html=True) 
        logging.warning("Logo Base64 decoding failed. Showing text fallback.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Sidebar Navigation
    with st.sidebar:
        st.title("Navigation")
        if st.session_state.get("user_id"):
             st.caption(f"Logged in as: {st.session_state['user_id']}")

        st.button("Home", on_click=lambda: st.session_state.update(page="home"))
        st.button("Own Wardrobe", on_click=lambda: st.session_state.update(page="wardrobe"))
        st.button("Account", on_click=lambda: st.session_state.update(page="profile"))
        st.button("Help", on_click=lambda: st.session_state.update(page="help"))
        st.button("Sign Out", on_click=sign_out)

def sign_out():
    """Clears session state and reruns."""
    st.session_state.clear()
    # Ensure all states are reset, especially the video state for next launch
    st.session_state["video_played"] = False 
    st.session_state["page"] = "intro_video"
    st.rerun()


def intro_video():
    """
    Plays the introductory video and auto-transitions.
    Uses byte loading and JavaScript for fullscreen effect.
    """
    
    # 1. Activate fullscreen mode CSS via JS
    st.components.v1.html("<script>setVideoMode(true);</script>", height=0)

    # 2. Read the video file as bytes for reliable loading
    video_bytes = None
    try:
        # Check if file exists first. If not, log and skip immediately.
        if not os.path.exists(MOCK_VIDEO_FILE):
            logging.error(f"Video file not found at path: {MOCK_VIDEO_FILE}. Skipping video.")
            st.warning(f"Video file '{MOCK_VIDEO_FILE}' not found. Starting app immediately.")
            st.session_state["video_played"] = True
            st.session_state["page"] = "login"
            st.rerun()
            return

        with open(MOCK_VIDEO_FILE, "rb") as f:
            video_bytes = f.read()
        logging.info(f"Successfully read video file: {MOCK_VIDEO_FILE}, size: {len(video_bytes)} bytes")

    except Exception as e:
        # Handle read errors (permissions, corruption)
        logging.error(f"Critical error loading video: {e}. Skipping video.")
        st.error("Error loading introductory video. Skipping...")
        st.session_state["video_played"] = True
        st.session_state["page"] = "login"
        st.rerun()
        return
        
    # 3. Display the video
    if video_bytes:
        # Display the video inside a fixed container controlled by CSS
        st.video(video_bytes, format="video/mp4", start_time=0)

        # 4. Auto-transition logic
        # We rely on a hidden state variable to track when the timer started.
        if "video_start_time" not in st.session_state:
            st.session_state["video_start_time"] = time.time()

        VIDEO_DURATION_SECONDS = 7 # Expected duration of 'starting video.mp4'
        time_elapsed = time.time() - st.session_state["video_start_time"]
        
        # Display progress using a status container for less visual disruption
        if time_elapsed < VIDEO_DURATION_SECONDS:
             # Use st.empty to hold the timer state and force a rerun
             with st.empty():
                 # Display a simple status message in the center of the screen
                 st.status(f"Loading Style Teller... Please wait {int(VIDEO_DURATION_SECONDS - time_elapsed) + 1} seconds.", state="running", expanded=True)
                 time.sleep(1) # Wait for 1 second before forcing a rerun
                 st.rerun()
        else:
            # Video finished, transition to login
            st.session_state["video_played"] = True
            st.session_state["video_start_time"] = None
            st.session_state["page"] = "login"
            st.rerun()

# --- Page Functions (Placeholders for now, focusing on core flow) ---

def login_signup():
    # Deactivate fullscreen mode CSS when showing the login page
    st.components.v1.html("<script>setVideoMode(false);</script>", height=0)
    
    # We explicitly place the logo here to ensure it's visible on the first non-video screen
    header()
    
    st.markdown("<h2 style='text-align: center;'>Welcome Back!</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Log in with Email/Password or Phone/OTP.</p>", unsafe_allow_html=True)

    auth_method = st.radio("Choose Login Method", ["Email / Password", "Phone / OTP"], index=0, horizontal=True)

    with st.container(border=True):
        if auth_method == "Email / Password":
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", use_container_width=True, key="email_login_btn"):
                    # Mock Login Logic
                    if email == "demo@example.com" and password == "password123":
                        st.session_state["logged_in"] = True
                        st.session_state["user_id"] = email
                        st.session_state["is_onboarding_complete"] = True # Assume demo user is complete
                        st.session_state["page"] = "home"
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")
            with col2:
                if st.button("Sign Up", use_container_width=True, key="email_signup_btn"):
                    st.info("Sign up is mocked for now. Use 'demo@example.com' / 'password123'")
        
        # --- Placeholder for Phone/OTP Logic ---
        # Note: OTP flow logic needs to be fully implemented here when requested. 
        # For now, it's a placeholder to complete the basic flow.
        elif auth_method == "Phone / OTP":
            st.info("Phone/OTP authentication coming soon. Please use Email/Password for now.")
            # phone_number = st.text_input("Phone Number (Mock)", key="login_phone")
            # if st.button("Send OTP", use_container_width=True, key="send_otp_btn"):
            #     # Mock OTP send logic
            #     st.session_state["otp_sent"] = True
            #     st.session_state["mock_phone"] = phone_number
            #     st.success(f"Mock OTP sent to {phone_number}. Use '1234'.")

            # if st.session_state["otp_sent"]:
            #     otp = st.text_input("Enter OTP (Mock: 1234)", key="login_otp")
            #     if st.button("Verify OTP & Login", use_container_width=True, key="verify_otp_btn"):
            #         if otp == "1234":
            #             st.session_state["logged_in"] = True
            #             st.session_state["user_id"] = st.session_state["mock_phone"]
            #             st.session_state["is_onboarding_complete"] = True 
            #             st.session_state["page"] = "home"
            #             st.success("Logged in successfully!")
            #             st.rerun()
            #         else:
            #             st.error("Invalid OTP.")


def user_details_screen():
    st.subheader("1. Tell us about yourself")
    # Form fields for user details here
    if st.button("Save Details & Next"):
        st.session_state["page"] = "choose_style"
        st.rerun()
        
def choose_style_screen():
    st.subheader("2. Choose Your Style")
    # Checkbox/Selectbox for style preferences here
    if st.button("Choose Style & Next"):
        st.session_state["page"] = "upload_image"
        st.rerun()

def upload_image_screen():
    st.subheader("3. Upload Your Image")
    st.warning("Upload logic needs to be implemented for avatar generation.")
    # File uploader component here
    if st.button("Upload & Next"):
        st.session_state["page"] = "all_set"
        st.rerun()

def all_set_screen():
    st.subheader("All Set! Welcome to Style Teller.")
    st.session_state["is_onboarding_complete"] = True
    if st.button("Go to Home"):
        st.session_state["page"] = "home"
        st.rerun()

def home_screen():
    st.subheader("Home Dashboard")
    st.info("Your personalized style recommendations will appear here.")

def wardrobe_app():
    st.subheader("Your Virtual Wardrobe")
    st.info("Manage your uploaded clothes. Feature coming soon.")

def show_avatar_outfits():
    st.subheader("Styled Outfits")
    st.info("View outfits generated for your avatar. Feature coming soon.")

def profile_screen():
    st.subheader("My Account")
    st.write(f"User ID: {st.session_state.get('user_id', 'N/A')}")
    st.info("Profile editing features coming soon.")

def help_screen():
    st.subheader("Help Center")
    st.write("For support, please contact help@styleteller.com.")

# --- Main Application Logic ---

def main():
    initialize_session_state()

    # Determine which screen to show
    current_page = st.session_state.get("page", "intro_video")
    
    # 1. Handle Video (if not played)
    if not st.session_state.get("video_played") and current_page == "intro_video":
        intro_video()
        # Immediately return after starting video/rerun
        return
    
    # 2. Deactivate fullscreen video mode once played/skipped
    # This must run every time we are NOT in the intro_video page
    # IMPORTANT: Do not remove this, it reverts the CSS needed for the main app view
    st.components.v1.html("<script>setVideoMode(false);</script>", height=0)


    # 3. Handle Authentication (if not logged in)
    if not st.session_state["logged_in"] and current_page not in ["login", "intro_video"]:
        # Force to login page if we have moved past the video
        st.session_state["page"] = "login"
        current_page = "login"

    # 4. Route Pages
    if current_page == "login":
        login_signup()
    elif current_page == "user_details":
        # Only show header for logged-in screens
        header()
        user_details_screen()
    elif current_page == "choose_style":
        header()
        choose_style_screen()
    elif current_page == "upload_image":
        header()
        upload_image_screen()
    elif current_page == "all_set":
        header()
        all_set_screen()
    elif current_page == "home":
        header()
        home_screen()
    elif current_page == "wardrobe":
        header()
        wardrobe_app()
    elif current_page == "style_outfits":
        header()
        show_avatar_outfits()
    elif current_page == "profile":
        header()
        profile_screen()
    elif current_page == "help":
        header()
        help_screen()
    
if __name__ == '__main__':
    main()
