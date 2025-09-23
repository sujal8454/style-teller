import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json
import os
import time
import base64
import random

def welcome_animation():
    """Renders a one-time welcome animation with an opening door video."""
    video_url = "https://youtube.com/shorts/4eBFn6PqAz0?feature=share" 
    

    st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');

            .stApp {{
                background-color: #000; /* Black background */
                overflow: hidden;
            }}
            #animation-container {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: #000;
                z-index: 9999;
            }}
            #welcome-video {{
                width: 100%;
                height: 100%;
                object-fit: cover; /* This makes the video cover the whole screen */
            }}
            .title-text {{
                position: absolute;
                font-family: 'Playfair Display', serif;
                font-size: 3rem;
                color: #e0c56e;
                text-shadow: 0 0 15px #e0c56e;
                opacity: 0;
                transition: opacity 1.5s ease-in-out;
                z-index: 10000;
            }}
            .fade-in {{
                opacity: 1;
            }}
        </style>

        <div id="animation-container">
            <video id="welcome-video" autoplay muted playsinline>
                <source src="{video_url}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <h1 id="title-text" class="title-text">Style Teller</h1>
        </div>

        <script>
            setTimeout(() => {{
                const video = document.getElementById('welcome-video');
                const titleText = document.getElementById('title-text');

                // When the video finishes playing
                video.addEventListener('ended', function() {{
                    // Fade in the title text
                    titleText.classList.add('fade-in');

                    // End the animation and signal Streamlit
                    setTimeout(() => {{
                        window.parent.postMessage({{
                            type: 'streamlit:setComponentValue',
                            key: 'animation_done_signal',
                            value: true
                        }}, '*');
                    }}, 2000); // Show title for 2 seconds
                }});

                // Fallback in case the video fails to load/play
                video.addEventListener('error', function() {{
                     window.parent.postMessage({{
                        type: 'streamlit:setComponentValue',
                        key: 'animation_done_signal',
                        value: true
                    }}, '*');
                }});

            }}, 100);
        </script>
    """, unsafe_allow_html=True, height=0)

    # This component is used to receive the signal from JavaScript
    st.session_state['animation_done_signal'] = st.session_state.get('animation_done_signal', False)
    if st.session_state['animation_done_signal']:
        st.session_state['animation_done'] = True


# --- Database and File Handling Functions ---

def save_user_db():
    """Saves the user database to a JSON file."""
    with open("user_db.json", "w") as f:
        json.dump(st.session_state.USER_DB, f)

def load_user_db():
    """Loads the user database from a JSON file, or creates a default one."""
    if os.path.exists("user_db.json"):
        with open("user_db.json", "r") as f:
            return json.load(f)
    return {
        "demo@example.com": {"password": "password123", "details": {"name": "Demo User", "age": 30, "gender": "Male", "styles": ["Formal"], "image_uploaded": True}},
        "alice@example.com": {"password": "stylequeen", "details": {"name": "Alice", "age": 25, "gender": "Female", "styles": ["Old money", "Casual"], "image_uploaded": True}},
        "bob@example.com": {"password": "fashionking", "details": {"name": "Bob", "age": 35, "gender": "Male", "styles": ["Streetwear", "Sporty"], "image_uploaded": True}}
    }

def save_remembered_user(email):
    """Saves the remembered email to a separate JSON file for persistence."""
    with open("remembered_user.json", "w") as f:
        json.dump({"email": email}, f)

def load_remembered_user():
    """Loads the remembered email from a JSON file."""
    if os.path.exists("remembered_user.json"):
        with open("remembered_user.json", "r") as f:
            data = json.load(f)
            return data.get("email", None)
    return None

def generate_ai_image(face_image, outfit_type, category):
    """Generates a placeholder AI image."""
    url = f"https://placehold.co/600x800.png?text={outfit_type}+{category}"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# --- Header and Navigation Functions ---

def header():
    """Renders the app header and navigation links."""
    st.markdown("""
    <style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .logo {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
    }
    .nav-links {
        display: flex;
        gap: 20px;
    }
    .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
    }
    .dropdown {
        position: relative;
        display: inline-block;
    }
    .dropdown-content {
        display: none;
        position: absolute;
        right: 0;
        background-color: #f9f9f9;
        min-width: 160px;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
        z-index: 1;
        border-radius: 5px;
    }
    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
        text-align: left;
    }
    .dropdown-content a:hover {background-color: #f1f1f1;}
    .show {display: block;}
    </style>
    """, unsafe_allow_html=True)

    header_html = """
    <div class="header">
        <div class="logo">Style Teller</div>
        <div class="nav-links">
            <a href="javascript:void(0);" onclick="goToHome()" class="nav-link">Home</a>
            <a href="javascript:void(0);" onclick="goToHelp()" class="nav-link">Help</a>
            <div class="dropdown">
                <a href="javascript:void(0);" onclick="toggleDropdown()" class="nav-link">Account</a>
                <div id="accountDropdown" class="dropdown-content">
                    <a href="javascript:void(0);" onclick="goToProfile()">Profile</a>
                    <a href="javascript:void(0);" onclick="goToSettings()">Settings</a>
                    <a href="javascript:void(0);" onclick="logout()">Log Out</a>
                </div>
            </div>
        </div>
    </div>

    <script>
    function toggleDropdown() {
        document.getElementById("accountDropdown").classList.toggle("show");
    }

    function goToHome() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'home'}, '*');
    }

    function goToHelp() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'help'}, '*');
    }

    function goToProfile() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'profile'}, '*');
    }

    function goToSettings() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'settings'}, '*');
    }

    function logout() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'logout'}, '*');
    }

    // Close the dropdown if clicked outside
    window.onclick = function(event) {
        if (!event.target.matches('.nav-link')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }
    </script>
    """

    st.markdown(header_html, unsafe_allow_html=True)

    if 'component_value' in st.session_state:
        if st.session_state['component_value'] == 'home':
            st.session_state["page"] = "home"
            st.session_state['component_value'] = None
            st.rerun()
        elif st.session_state['component_value'] == 'profile':
            st.session_state["page"] = "profile"
            st.session_state['component_value'] = None
            st.rerun()
        elif st.session_state['component_value'] == 'settings':
            st.session_state["page"] = "settings"
            st.session_state['component_value'] = None
            st.rerun()
        elif st.session_state['component_value'] == 'help':
            st.session_state["page"] = "help"
            st.session_state['component_value'] = None
            st.rerun()
        elif st.session_state['component_value'] == 'logout':
            st.session_state["logged_in"] = False
            st.session_state['component_value'] = None
            st.rerun()

# --- Login and Signup Functions ---

def login_signup():
    """Renders the login and signup page."""
    st.title("Style Teller")

    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    .stTextInput > div > div > input, .stTextInput label {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
    }
    .stRadio > div, .stRadio label, .stCheckbox > div, .stCheckbox label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .stTitle {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Email/Password", "Phone/OTP"])

    with tab1:
        auth_mode = st.radio("Select an option", ["Login", "Sign Up"], horizontal=True)

        # Pre-fill email if it's remembered
        remembered_email = st.session_state.get("remembered_email", "")
        email = st.text_input("Email", value=remembered_email)
        password = st.text_input("Password", type="password")

        remember_me = st.checkbox("Remember me", value=bool(remembered_email))

        if auth_mode == "Login":
            if st.button("Login", key="email_login"):
                if email in st.session_state.USER_DB and st.session_state.USER_DB[email]['password'] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = email

                    if remember_me:
                        save_remembered_user(email)
                    else:
                        if os.path.exists("remembered_user.json"):
                            os.remove("remembered_user.json")

                    st.session_state["show_welcome"] = True
                    st.session_state["welcome_time"] = time.time()

                    # Check if user details are already provided
                    if st.session_state.USER_DB[email]['details']:
                        st.session_state["onboarding_complete"] = True
                        st.session_state["page"] = "home"
                    else:
                        st.session_state["details_provided"] = False
                        st.session_state["page"] = "user_details"
                    st.rerun()

                else:
                    st.error("Invalid email or password.")
        else:
            password_confirm = st.text_input("Confirm Password", type="password")

            if st.button("Sign Up", key="email_signup"):
                if email in st.session_state.USER_DB:
                    st.error("Email already registered.")
                elif not "@" in email or not "." in email:
                    st.error("Please enter a valid email address.")
                elif len(password) < 8:
                    st.error("Password must be at least 8 characters long.")
                elif password != password_confirm:
                    st.error("Passwords do not match.")
                else:
                    st.session_state.USER_DB[email] = {"password": password, "details": None}
                    save_user_db()

                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = email
                    st.session_state["details_provided"] = False

                    if remember_me:
                        save_remembered_user(email)
                    else:
                        if os.path.exists("remembered_user.json"):
                            os.remove("remembered_user.json")

                    st.session_state["show_welcome"] = True
                    st.session_state["welcome_time"] = time.time()
                    st.session_state["page"] = "user_details"
                    st.rerun()

    with tab2:
        st.subheader("Login with Phone Number")
        phone_number = st.text_input("Phone Number", placeholder="e.g., +15551234567")

        if st.button("Send OTP", key="send_otp"):
            if not phone_number:
                st.error("Please enter a phone number.")
            else:
                # Simulate OTP generation and sending
                otp = str(random.randint(1000, 9999))
                st.session_state["otp"] = otp
                st.session_state["otp_sent"] = True
                st.success(f"An OTP has been sent to {phone_number}. (Simulated OTP: {otp})")

        if st.session_state.get("otp_sent"):
            otp_input = st.text_input("Enter OTP", type="password")

            if st.button("Verify OTP", key="verify_otp"):
                if otp_input == st.session_state.get("otp"):
                    if phone_number not in st.session_state.PHONE_DB:
                        st.session_state.PHONE_DB[phone_number] = "verified"
                        st.info("New account created for this phone number.")

                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = phone_number
                    st.session_state["show_welcome"] = True
                    st.session_state["welcome_time"] = time.time()

                    st.session_state["otp_sent"] = False  # Reset OTP state
                    st.session_state["details_provided"] = False
                    st.session_state["page"] = "user_details"
                    st.rerun()
                else:
                    st.error("Invalid OTP. Please try again.")

    if st.session_state.get('notification_status') == 'ask':
        st.markdown("""
            <style>
                .notification-bar {
                    position: fixed;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 90%;
                    max-width: 400px;
                    background-color: rgba(255, 255, 255, 0.9);
                    color: black;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                    z-index: 10000;
                    display: block; /* Initially visible */
                    text-align: left;
                    border: 1px solid #ddd;
                }
                .notification-bar h4 {
                    margin: 0 0 10px 0;
                    font-weight: bold;
                    color: #000;
                }
                .notification-bar p {
                    margin: 0;
                    opacity: 1;
                    transition: opacity 0.5s;
                    color: #333;
                }
                .notification-buttons {
                    margin-top: 15px;
                    display: flex;
                    justify-content: flex-end;
                    gap: 10px;
                }
                .notification-btn {
                    background: none;
                    border: none;
                    color: #4CAF50; /* Green accent color */
                    font-weight: bold;
                    cursor: pointer;
                    padding: 5px;
                    font-size: 1rem;
                }
                #notification-success {
                    display: none; /* Hidden by default */
                }
            </style>

            <div id="notification-bar" class="notification-bar">
                <div id="notification-prompt">
                    <h4><b>Notification</b></h4>
                    <div class="notification-buttons">
                        <button id="block-btn" class="notification-btn">Block</button>
                        <button id="allow-btn" class="notification-btn">Allow</button>
                    </div>
                </div>
                <div id="notification-success">
                    <p>Notifications are enabled! You'll receive personalized updates and exclusive deals.</p>
                </div>
            </div>

            <script>
                setTimeout(() => {
                    const notificationBar = document.getElementById('notification-bar');
                    const promptDiv = document.getElementById('notification-prompt');
                    const successDiv = document.getElementById('notification-success');
                    const allowBtn = document.getElementById('allow-btn');
                    const blockBtn = document.getElementById('block-btn');

                    if (notificationBar) {
                        allowBtn.addEventListener('click', () => {
                            promptDiv.style.display = 'none';
                            successDiv.style.display = 'block';

                            // Send 'allowed' status back to Streamlit
                            window.parent.postMessage({
                                type: 'streamlit:setComponentValue',
                                key: 'notification_status_signal',
                                value: 'allowed'
                            }, '*');

                            // Hide the bar after a few seconds
                            setTimeout(() => {
                                if (notificationBar) {
                                    notificationBar.style.display = 'none';
                                }
                            }, 3000);
                        });

                        blockBtn.addEventListener('click', () => {
                            if (notificationBar) {
                                notificationBar.style.display = 'none';
                            }
                            // Send 'blocked' status back to Streamlit
                             window.parent.postMessage({
                                type: 'streamlit:setComponentValue',
                                key: 'notification_status_signal',
                                value: 'blocked'
                            }, '*');
                        });
                    }
                }, 100);
            </script>
        """, unsafe_allow_html=True)

def user_details_screen():
    """Renders the page to collect user's name, age, and gender."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    .stTextInput > div > div > input, .stTextInput label {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
    }
    .stRadio > div, .stRadio label, .stCheckbox > div, .stCheckbox label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .stTitle {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Tell Us About Yourself")
    st.markdown("<div class='text-with-bg'>Please provide a few details to get the most personalized style recommendations.</div>", unsafe_allow_html=True)

    with st.form("user_details_form"):
        name = st.text_input("Name", placeholder="Your Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        gender = st.radio("Gender", ["Male", "Female", "Other"])

        submitted = st.form_submit_button("Save and Continue")

        if submitted:
            if not name or not age:
                st.error("Please fill in your name and age.")
            else:
                user_id = st.session_state["current_user"]
                if user_id in st.session_state.USER_DB:
                    st.session_state.USER_DB[user_id]['details'] = {
                        "name": name,
                        "age": age,
                        "gender": gender,
                        "styles": [],
                        "image_uploaded": False
                    }
                else:
                    st.session_state.USER_DB[user_id] = {
                        "details": {
                            "name": name,
                            "age": age,
                            "gender": gender,
                            "styles": [],
                            "image_uploaded": False
                        }
                    }
                save_user_db()
                st.session_state["details_provided"] = True
                st.session_state["page"] = "choose_style"
                st.rerun()

def choose_style_screen():
    """Renders the page for the user to choose their preferred styles."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    .stTextInput > div > div > input, .stTextInput label {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
    }
    .stRadio > div, .stRadio label, .stCheckbox > div, .stCheckbox label {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .stTitle {
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px #000000;
    }
    .stButton > button {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Choose Your Style")
    st.markdown("<div class='text-with-bg'>Select the styles that best match your personality.</div>", unsafe_allow_html=True)

    styles = ["Indian", "Old money", "Streetwear", "Sporty", "Formal", "Casual"]

    with st.form("style_form"):
        selected_styles = st.multiselect("Select at least one style", styles)
        submitted = st.form_submit_button("Save and Continue")

        if submitted:
            if not selected_styles:
                st.error("Please choose at least one style.")
            else:
                user_id = st.session_state["current_user"]
                st.session_state.USER_DB[user_id]['details']['styles'] = selected_styles
                save_user_db()
                st.session_state["styles_chosen"] = True
                st.session_state["page"] = "upload_image"
                st.rerun()

def upload_image_screen():
    """Renders the page for the user to upload a full-body image."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    h1, h2, h3, p {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .instruction-header {
        font-weight: bold;
        color: #FFFFFF !important;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Upload Your Image")
    st.markdown("<div class='text-with-bg'>Upload a photo for a more personalized style analysis.</div>", unsafe_allow_html=True)

    with st.form("image_upload_form"):
        uploaded_image = st.file_uploader("Upload your full-body image", type=["jpg", "png", "jpeg"])

        st.markdown("<h3 class='instruction-header'>Image Description</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='text-with-bg'>
        <ul>
            <li>
                <strong>Full body Shot:</strong> Show your complete outfit from Head to toe for complete style analysis.
            </li>
            <li>
                <strong>Plain background:</strong> Use a simple, Uncluttered background to help our AI focus on your style.
            </li>
            <li>
                <strong>Decent Lighting:</strong> Click in natural light- avoid dark and shadow areas for a clear photo.
            </li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button("Save and Continue")

        if submitted:
            if not uploaded_image:
                st.error("Please upload an image to continue.")
            else:
                user_id = st.session_state["current_user"]
                st.session_state.USER_DB[user_id]['details']['image_uploaded'] = True
                # In a real app, you would save the image data here.
                # For this demo, we just mark it as complete.
                save_user_db()
                st.session_state["image_uploaded"] = True
                st.session_state["page"] = "all_set"
                st.rerun()

def all_set_screen():
    """Renders the final confirmation page."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    .tick-circle {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #4CAF50;
        border-radius: 50%;
        width: 100px;
        height: 100px;
        margin: 20px auto;
        color: white;
        font-size: 60px;
        font-weight: bold;
    }
    .all-set-text {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #FFFFFF !important;
        text-shadow: 2px 2px 4px #000000;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='tick-circle'>✓</div>", unsafe_allow_html=True)
    st.markdown("<p class='all-set-text'>You're All Set!</p>", unsafe_allow_html=True)

    if st.button("Go to Home"):
        st.session_state["onboarding_complete"] = True
        st.session_state["page"] = "home"
        st.rerun()

# --- App Screens ---

def home_screen():
    """Renders the main home screen of the app."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    .stTextInput > div > div > input, .stTextInput label {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
    }
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.7) !important;
        color: #000000 !important;
    }
    h1, h2, h3, p {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    header()

    user_id = st.session_state["current_user"]
    if st.session_state.USER_DB.get(user_id) and st.session_state.USER_DB[user_id]['details']:
        user_name = st.session_state.USER_DB[user_id]['details']['name']
    else:
        user_name = user_id.split('@')[0] if '@' in user_id else "Guest"

    if "show_welcome" in st.session_state and st.session_state["show_welcome"]:
        current_time = time.time()
        if current_time - st.session_state["welcome_time"] < 2:
            st.success(f"Welcome back, {user_name}!")
            st.balloons()
        else:
            st.session_state["show_welcome"] = False

    st.title("🧥 Style Teller")
    st.markdown(f"<div class='text-with-bg'>Welcome to your AI-powered virtual wardrobe, {user_name}!</div>", unsafe_allow_html=True)

    st.subheader("Featured Styles")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Formal", key="formal_btn"):
            st.session_state["page"] = "wardrobe"
            st.session_state["preset_style"] = "Formal"
            st.rerun()
        st.image("https://placehold.co/300x400.png?text=Formal", use_column_width=True)
    with col2:
        if st.button("Old Money", key="oldmoney_btn"):
            st.session_state["page"] = "wardrobe"
            st.session_state["preset_style"] = "Old Money"
            st.rerun()
        st.image("https://placehold.co/300x400.png?text=Old+Money", use_column_width=True)
    with col3:
        if st.button("Casual", key="casual_btn"):
            st.session_state["page"] = "wardrobe"
            st.session_state["preset_style"] = "Casual"
            st.rerun()
        st.image("https://placehold.co/300x400.png?text=Casual", use_column_width=True)

    st.subheader("Recent Outfits")
    st.markdown("<div class='text-with-bg'>Create your first outfit to see it here!</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create New Outfit"):
            st.session_state["page"] = "wardrobe"
            st.rerun()
    with col2:
        if st.button("Create Your Own Outfit"):
            st.session_state["page"] = "wardrobe"
            st.session_state["custom_outfit"] = True
            st.rerun()

def profile_screen():
    """Renders the user profile screen."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    h1, h2, h3, p {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    header()

    st.title("Profile")
    user_id = st.session_state["current_user"]
    user_details = st.session_state.USER_DB.get(user_id, {}).get('details', {})

    user_email = user_id
    user_name = user_details.get("name", "N/A")
    user_age = user_details.get("age", "N/A")
    user_gender = user_details.get("gender", "N/A")
    user_styles = ", ".join(user_details.get("styles", ["N/A"]))

    st.subheader("Account Information")
    st.markdown(f"<div class='text-with-bg'><strong>Email/Phone:</strong> {user_email}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='text-with-bg'><strong>Name:</strong> {user_name}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='text-with-bg'><strong>Age:</strong> {user_age}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='text-with-bg'><strong>Gender:</strong> {user_gender}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='text-with-bg'><strong>Preferred Styles:</strong> {user_styles}</div>", unsafe_allow_html=True)

    st.subheader("Profile Settings")
    new_name = st.text_input("Display Name", value=user_name)

    if st.button("Update Profile"):
        st.success("Profile updated successfully!")

    st.subheader("Your Style Preferences")
    st.markdown("<div class='text-with-bg'>You haven't set any style preferences yet.</div>", unsafe_allow_html=True)

    if st.button("Go to Home"):
        st.session_state["page"] = "home"
        st.rerun()

def settings_screen():
    """Renders the settings screen."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    h1, h2, h3, p {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    header()

    st.title("Settings")

    st.subheader("Account Settings")
    st.checkbox("Remember login credentials", value=True)
    st.checkbox("Email notifications", value=True)

    st.subheader("Theme Settings")
    theme = st.selectbox("Select Theme", ["Light", "Dark", "Auto"])

    st.subheader("Privacy")
    st.checkbox("Allow data collection for personalized recommendations", value=True)

    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

    st.subheader("Danger Zone")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        if "remembered_email" in st.session_state:
            del st.session_state["remembered_email"]
        st.rerun()

    if st.button("Delete Account", key="delete_account"):
        st.error("This will permanently delete your account and all your data.")
        if st.button("Confirm Delete", key="confirm_delete"):
            email = st.session_state["current_user"]
            if email in st.session_state.USER_DB:
                del st.session_state.USER_DB[email]
                save_user_db()
                st.session_state["logged_in"] = False
                st.rerun()

def help_screen():
    """Renders the help screen."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    h1, h2, h3, p, li {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    header()

    st.title("Help & FAQ")

    with st.expander("How to Use Style Teller", expanded=True):
        st.markdown("""
        <div class='text-with-bg'>
        <p><strong>Step 1:</strong> Click on "Create New Outfit" from the home screen</p>
        <p><strong>Step 2:</strong> Upload a clear photo of your face</p>
        <p><strong>Step 3:</strong> Select your body type, skin tone, and style preferences</p>
        <p><strong>Step 4:</strong> Click "Generate Outfits" to see AI recommendations</p>
        <p><strong>Step 5:</strong> Save or download outfits you like</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Adding Your Own Items", expanded=False):
        st.markdown("""
        <div class='text-with-bg'>
        <p>You can add your own clothing items to create custom outfits:</p>
        <p><strong>1. Text Search:</strong> Search for items by description</p>
        <p><strong>2. Photo Library:</strong> Upload photos from your device</p>
        <p><strong>3. Camera:</strong> Take photos directly using your device camera</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Downloading Outfits", expanded=False):
        st.markdown("""
        <div class='text-with-bg'>
        <p>To download an outfit:</p>
        <p>1. Generate your desired outfit</p>
        <p>2. Click the "Download" button under the outfit image</p>
        <p>3. Choose your preferred image format</p>
        <p>4. Save to your device</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Frequently Asked Questions")

    with st.expander("Is my photo data secure?", expanded=False):
        st.markdown("""
        <div class='text-with-bg'>
        All uploaded photos are processed securely and are not shared with third parties.
        Your privacy is our top priority.
        </div>
        """, unsafe_allow_html=True)

    with st.expander("How accurate are the outfit recommendations?", expanded=False):
        st.markdown("""
        <div class='text-with-bg'>
        Our AI system continuously learns and improves. The recommendations take into account
        your body type, skin tone, preferences, and current fashion trends to provide the most
        suitable options.
        </div>
        """, unsafe_allow_html=True)

    if st.button("Return to Home"):
        st.session_state["page"] = "home"
        st.rerun()

def wardrobe_app():
    """Renders the wardrobe creation screen."""
    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    .stTextInput > div > div > input, .stTextInput label {
        color: #000000 !important;
        background-color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 500 !important;
    }
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.7) !important;
        color: #000000 !important;
    }
    h1, h2, h3, p {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .instruction-header {
        font-weight: bold;
        color: #4CAF50 !important;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    header()

    st.title("🧥 Create Your Outfit")

    with st.expander("📸 Upload Your Face", expanded=True):
        st.markdown("<h3 class='instruction-header'>INSTRUCTIONS</h3>", unsafe_allow_html=True)
        st.markdown("<div class='text-with-bg'>Upload a clear front-facing photo with your full face visible, eyes open, and no blurriness.</div>", unsafe_allow_html=True)

        face_image = st.file_uploader("Upload face image", type=["jpg", "png"])
        if face_image:
            img = Image.open(face_image)
            st.image(img, caption="Your uploaded image", width=200)

    # Add Your Own Items section
    with st.expander("Add Your Own Items", expanded=True):
        st.markdown("<div class='text-with-bg'>Add your own clothing items to create custom outfits</div>", unsafe_allow_html=True)

        add_items_tab1, add_items_tab2, add_items_tab3 = st.tabs(["Text Search", "Photo Library", "Camera"])

        with add_items_tab1:
            st.text_input("Search for items", placeholder="e.g., blue jeans, white shirt")
            if st.button("Search"):
                st.info("Searching for items...")

        with add_items_tab2:
            st.file_uploader("Upload clothing items", type=["jpg", "png"], accept_multiple_files=True)

        with add_items_tab3:
            if st.camera_input("Take a photo of your clothing item"):
                st.success("Photo captured successfully!")

    preset_style = st.session_state.get("preset_style", None)

    body_type = st.selectbox("Choose Your Body Type", ["Slim", "Athletic", "Curvy", "Plus-size"])
    gender = st.radio("Select Gender", ["Male", "Female", "Other"])

    skin_tones = {
        "Very Fair": "#FFDBAC",
        "Fair": "#F1C27D",
        "Medium": "#E0AC69",
        "Olive": "#C68642",
        "Brown": "#8D5524",
        "Dark Brown": "#5C3836",
        "Very Dark": "#402218"
    }
    selected_tone = st.selectbox("Choose Your Skin Tone", list(skin_tones.keys()))
    body_color = skin_tones[selected_tone]
    st.color_picker("Preview Skin Tone", body_color, disabled=True)

    color_choice = st.text_input("Optional: Favorite color palette")

    # Add age selection
    age_range = st.selectbox("Age Range", [
        "Under 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65+"
    ])

    style_options = ["Formal", "Old Money", "Casual", "Business Casual"]
    outfit_type = st.selectbox("Style Type", style_options,
                              index=style_options.index(preset_style) if preset_style in style_options else 0)

    occasion = st.selectbox("Occasion", [
        "Wedding", "Job Interview", "Date Night", "Party",
        "Office", "Casual Outing", "Vacation", "Outdoor Event"
    ])

    if st.button("Generate Outfits"):
        if face_image:
            # Set session state to show outfit screen
            st.session_state["page"] = "outfit_results"
            st.session_state["outfit_data"] = {
                "face_image": face_image,
                "outfit_type": outfit_type,
                "occasion": occasion,
                "age_range": age_range  # Add age range to the outfit data
            }
            st.rerun()
        else:
            st.warning("Please upload your face photo.")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """
    Generate HTML code for a download link
    """
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}" class="download-btn">Download {file_label}</a>'
    return href

def outfit_results():
    """Renders the outfit generation results screen."""
    face_image = st.session_state["outfit_data"]["face_image"]
    outfit_type = st.session_state["outfit_data"]["outfit_type"]
    occasion = st.session_state["outfit_data"]["occasion"]
    age_range = st.session_state["outfit_data"].get("age_range", "25-34")  # Default age range if not provided

    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://i.postimg.cc/VkfS9X7d/temp-Imagegq-CSdo.avif');
        background-size: cover;
        background-attachment: fixed;
    }
    h1, h2, h3, p {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px #000000;
    }
    .outfit-card {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 15px;
    }
    .download-btn {
        display: inline-block;
        padding: 8px 16px;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        border-radius: 4px;
        margin-top: 8px;
        font-weight: bold;
    }
    .text-with-bg {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    header()

    st.title("Your AI-Generated Outfits")

    st.success(f"Here are your {outfit_type} outfits for {occasion}")

    st.subheader("Virtual Try-On")

    # Generate outfit image
    try_on_img = "https://placehold.co/800x1000.png?text=AI+Generated+Face+With+Outfit"
    st.image(try_on_img, caption="AI-generated image of you in the outfit", use_column_width=True)

    # Create a BytesIO object to store the image for download
    img_response = requests.get(try_on_img)
    img_bytes = BytesIO(img_response.content)

    # Add download button
    st.markdown("<div class='text-with-bg'>Download this outfit to your device</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Download as PNG"):
            st.markdown(
                get_binary_file_downloader_html(img_bytes.getvalue(), f"style_teller_outfit_{outfit_type}.png"),
                unsafe_allow_html=True
            )
    with col2:
        if st.button("Download as JPG"):
            img = Image.open(img_bytes)
            jpg_bytes = BytesIO()
            img.convert('RGB').save(jpg_bytes, format='JPEG')
            st.markdown(
                get_binary_file_downloader_html(jpg_bytes.getvalue(), f"style_teller_outfit_{outfit_type}.jpg"),
                unsafe_allow_html=True
            )

    if st.button("Generate More Options"):
        st.info("Generating additional outfits...")

    categories = ["Topwear", "Bottomwear", "Full Outfit", "Accessories"]

    for category in categories:
        st.subheader(f"{category} Options")

        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                img = generate_ai_image(face_image, outfit_type, f"{category}_{i+1}")
                st.image(img, caption=f"Option {i+1}", use_column_width=True)
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.button(f"Save {i+1}", key=f"save_{category}_{i}")
                with col2:
                    # Add download button for each item
                    if st.button(f"Download {i+1}", key=f"download_{category}_{i}"):
                        item_img_bytes = BytesIO()
                        img.save(item_img_bytes, format='PNG')
                        st.markdown(
                            get_binary_file_downloader_html(item_img_bytes.getvalue(), f"{category}_option_{i+1}.png"),
                            unsafe_allow_html=True
                        )

def main():
    """Main function to run the app."""
    st.set_page_config(page_title="Style Teller", layout="centered", page_icon="🧥")

    # Initialize session state variables if they don't exist
    if "animation_done" not in st.session_state:
        st.session_state['animation_done'] = False
        
    if not st.session_state['animation_done']:
        welcome_animation()
        return # Stop execution until animation is done

    # Initialize session state for notification preference
    if 'notification_status' not in st.session_state:
        st.session_state['notification_status'] = 'ask'

    # Component to listen for JS signal for notifications
    st.session_state['notification_status_signal'] = st.session_state.get('notification_status_signal', None)

    # Handle the signal from JS
    if st.session_state['notification_status_signal']:
        st.session_state['notification_status'] = st.session_state['notification_status_signal']
        st.session_state['notification_status_signal'] = None # Reset signal
        st.rerun() # Rerun to apply the state change

    # --- The rest of the app logic runs after the animation ---

    if "USER_DB" not in st.session_state:
        st.session_state.USER_DB = load_user_db()

    if "PHONE_DB" not in st.session_state:
        st.session_state.PHONE_DB = {
            "+15551112222": "verified",
            "+15553334444": "verified"
        }

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Onboarding step trackers
    if "details_provided" not in st.session_state:
        st.session_state["details_provided"] = False
    if "styles_chosen" not in st.session_state:
        st.session_state["styles_chosen"] = False
    if "image_uploaded" not in st.session_state:
        st.session_state["image_uploaded"] = False
    if "onboarding_complete" not in st.session_state:
        st.session_state["onboarding_complete"] = False

    # Load remembered email from persistent storage at app start
    if "remembered_email" not in st.session_state:
        st.session_state["remembered_email"] = load_remembered_user()

    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    # Handle navigation from the header component
    component_value = st.session_state.get("component_value")
    if component_value == "home":
        st.session_state["page"] = "home"
    elif component_value == "profile":
        st.session_state["page"] = "profile"
    elif component_value == "settings":
        st.session_state["page"] = "settings"
    elif component_value == "logout":
        st.session_state["logged_in"] = False
        # Remove the remembered user file on logout
        if os.path.exists("remembered_user.json"):
            os.remove("remembered_user.json")

    # Automatically log in the user if a remembered email exists and is valid
    if not st.session_state["logged_in"] and st.session_state["remembered_email"]:
        email = st.session_state["remembered_email"]
        if email in st.session_state.USER_DB and st.session_state.USER_DB[email].get('password'):
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = email
            # Set onboarding flags based on existing data
            if st.session_state.USER_DB[email]['details']:
                st.session_state["details_provided"] = True
                if st.session_state.USER_DB[email]['details']['styles']:
                    st.session_state["styles_chosen"] = True
                if st.session_state.USER_DB[email]['details']['image_uploaded']:
                    st.session_state["image_uploaded"] = True
                    st.session_state["onboarding_complete"] = True

    # Display the correct page based on login status and details provided
    if not st.session_state["logged_in"]:
        login_signup()
    else:
        # Onboarding flow for new users
        user_id = st.session_state["current_user"]
        if st.session_state.USER_DB.get(user_id) and st.session_state.USER_DB[user_id]['details'] is None:
            st.session_state["page"] = "user_details"
            st.session_state["details_provided"] = False

        if not st.session_state.get("details_provided"):
            user_details_screen()
        elif not st.session_state.get("styles_chosen"):
            choose_style_screen()
        elif not st.session_state.get("image_uploaded"):
            upload_image_screen()
        elif not st.session_state.get("onboarding_complete"):
            all_set_screen()
        else:
            if st.session_state["page"] == "home":
                home_screen()
            elif st.session_state["page"] == "wardrobe":
                wardrobe_app()
            elif st.session_state["page"] == "outfit_results":
                outfit_results()
            elif st.session_state["page"] == "profile":
                profile_screen()
            elif st.session_state["page"] == "settings":
                settings_screen()
            elif st.session_state["page"] == "help":
                help_screen()
            elif st.session_state["page"] == "user_details":
                user_details_screen()

if __name__ == "__main__":
    main()
