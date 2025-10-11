import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json
import os
import time
import base64
import random

# --- NEW ASSET LINKS ---
INTRO_IMAGE_URL = "https://ibb.co/B5qxJWW8" # Requested Still Image
BACKGROUND_IMAGE_URL = "https://ibb.co/gMDjN4Mt" # Requested Background Image
NEW_LOGO_URL = "https://ibb.co/3YMDZQVn" # Requested New Logo
# NOTE: Cannot directly host audio in Python/Streamlit without an external file/service.
# The music requirement will be represented by a placeholder comment in the code.

# --- Database and File Handling Functions (Retained) ---

# Note: In a real-world scenario, these files would be stored in a cloud environment (like S3 or Google Cloud Storage)
# for persistence across Streamlit app restarts. For this environment, we rely on local file persistence.

def save_user_db():
    """Saves the user database to a JSON file."""
    try:
        with open("user_db.json", "w") as f:
            json.dump(st.session_state.USER_DB, f)
    except Exception as e:
        # Catch exception in case of file system limitations
        print(f"Error saving user DB: {e}")

def load_user_db():
    """Loads the user database from a JSON file, or creates a default one."""
    if os.path.exists("user_db.json"):
        try:
            with open("user_db.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading user DB, using default: {e}")
            pass
    return {
        "demo@example.com": {"password": "password123", "details": {"name": "Demo User", "age": 30, "gender": "Male", "styles": ["Formal"], "image_uploaded": True}},
        "alice@example.com": {"password": "stylequeen", "details": {"name": "Alice", "age": 25, "gender": "Female", "styles": ["Old money", "Casual"], "image_uploaded": True}},
        "bob@example.com": {"password": "fashionking", "details": {"name": "Bob", "age": 35, "gender": "Male", "styles": ["Streetwear", "Sporty"], "image_uploaded": True}}
    }

# --- Custom Styling (Includes UI Fixes and Transitions) ---

def set_styles():
    """Sets the custom CSS for the app, incorporating new background, colors, and transitions."""
    
    # --- Critical Style Updates ---
    
    # 5. Background Update - NOTE: Replacing ibb.co with i.ibb.co for direct image linking
    background_url = BACKGROUND_IMAGE_URL.replace("ibb.co", "i.ibb.co")
    
    # 3. Logo Update - NOTE: Replacing ibb.co with i.ibb.co for direct image linking
    logo_url = NEW_LOGO_URL.replace("ibb.co", "i.ibb.co")
    
    # 1. Intro Image Fade-in/Fade-out CSS
    intro_image_css = f"""
    @keyframes fadein-intro {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}
    @keyframes fadeout-intro {{
        0% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
    }}
    .intro-screen {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 99999;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #000000; /* Ensure black background during transition */
    }}
    .intro-image {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        animation: fadein-intro 1.5s ease-in-out 0s 1 normal forwards; /* Fade-in (1.5s) */
    }}
    .intro-fade-out .intro-image {{
        animation: fadeout-intro 1s ease-in-out 0s 1 normal forwards; /* Fade-out (1s) */
    }}
    """
    
    # 2. & 3. Page-Load and Logo Fade-in CSS
    # 5. Background Overlay
    page_fade_css = f"""
    @keyframes fadein-page {{
        0% {{ opacity: 0; }}
        100% {{ opacity: 1; }}
    }}
    
    .stApp {{
        /* 5. Background properties */
        background-image: url({background_url});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    
    /* 5. Soft white overlay (10-20% opacity) */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255, 255, 255, 0.15); /* 15% white overlay */
        z-index: -1;
    }}

    /* 2. Gentle fade-in transition (1 second) for entire page content */
    div[data-testid="stAppViewContainer"] > div:first-child {{
        animation: fadein-page 1s ease-out 0s 1 normal forwards;
    }}
    
    /* 3. Logo Placement and Animation */
    .logo-container {{
        text-align: center;
        width: 100%;
        padding-top: 10px; /* Space from top */
        padding-bottom: 10px;
        animation: fadein-page 1s ease-out 0s 1 normal forwards; /* Sync with page fade-in */
        opacity: 0; /* Start hidden for animation */
    }}
    .logo-container img {{
        max-height: 50px; /* Adjust height as needed, keep proportionate */
        width: auto;
    }}
    """
    
    # 4. Color & UI Updates (White Boxes, Black Text, No Dark Elements)
    color_ui_css = """
        /* Global Text Color: Ensure ALL text is BLACK (Req 4) */
        div, span, p, a, label, h1, h2, h3, h4, .stApp, 
        .st-emotion-cache-12fmw6v, 
        .st-emotion-cache-1fsy711 > div, 
        div[data-testid="stAppViewContainer"] *, 
        .stMarkdown, 
        .stText,
        .stBlock *, 
        .rules-section strong, 
        .rules-section p 
        {
            color: #000000 !important; /* Force all text to black */
        }
        
        /* 4. Change all black/dark boxes to PURE WHITE (#FFFFFF) */
        
        /* Target the actual input element for text, number, and password fields */
        div[data-baseweb="input"] input,
        div[data-baseweb="input"] textarea,
        div[data-baseweb="base-input"] input, 
        input[type="text"], 
        input[type="password"],
        input[type="number"],
        textarea {
            background-color: #ffffff !important; 
            border: 1px solid #e0e0e0 !important; 
        }
        
        /* Ensure the input container also respects the white theme */
        div[data-testid="stTextInput"] > div > div, 
        div[data-testid="stNumberInput"] > div > div,
        div[data-testid="stSelectbox"] > div,
        div[data-baseweb="input"] {
            background-color: #ffffff !important;
        }
        
        /* Selectbox/Dropdown Display Text: Ensure selected option text is BLACK */
        div[data-testid="stSelectbox"] div[data-baseweb="select"] input {
             color: #000000 !important;
        }

        /* --- BUTTON STYLING OVERRIDE (White Buttons/Black Text) --- */

        /* Target all common button containers, including primary and secondary */
        div[data-testid="stVerticalBlock"] .st-emotion-cache-1v0bb6x, 
        .st-emotion-cache-1v0bb6x, 
        .st-emotion-cache-7ym5gk, 
        div[data-testid*="stButton"] > button
        {
            background-color: #ffffff !important; /* White background */
            color: #000000 !important; /* Black text */
            border: 1px solid #000000 !important; /* Black border for distinction */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        .st-emotion-cache-1v0bb6x:hover, 
        .st-emotion-cache-7ym5gk:hover,
        div[data-testid*="stButton"] > button:hover {
            color: #000000 !important; 
            border: 1px solid #000000 !important; 
            background-color: #f0f0f0 !important; 
        }
        
        /* --- General Dark Container Fixes (Forms, Alerts, etc.) --- */
        div.st-emotion-cache-6o6vcr, 
        div[data-testid="stForm"], 
        div[data-testid="stAlert"],
        div[data-baseweb="popover"], 
        div[role="listbox"], 
        .st-emotion-cache-1fcpj1c, 
        .st-emotion-cache-16j94j4, 
        div[data-testid="stVerticalBlock"],
        .outfit-card /* Ensure outfit cards are white */
        {
            background-color: #ffffff !important; 
            border: 1px solid #e0e0e0; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        /* Sidebar/Dark UI Element Fix (Sidebar itself must be white) */
        div[data-testid="stSidebar"] {
            background-color: #ffffff !important; /* White sidebar */
            border-right: 1px solid #e0e0e0; /* Add a divider */
        }
        
        /* Ensure sidebar text remains black on the new white sidebar */
        div[data-testid="stSidebar"] *, 
        div[data-testid="stSidebarContent"] button {
             color: #000000 !important; 
             background-color: transparent !important;
             border: none !important;
        }

        /* Standard Layout CSS */

        .st-emotion-cache-j93igk {
            border-bottom: 2px solid #ccc;
        }
        
        /* Default container styling (Now white via global fix) */
        div.st-emotion-cache-6o6vcr {
            border-radius: 10px;
            padding: 20px;
        }

        .st-emotion-cache-11r9w7n, .st-emotion-cache-11r9w7n .st-bm {
            width: 100%;
        }

        .st-emotion-cache-13srm2a .st-emotion-cache-7ym5gk {
            margin: 10px 0;
        }

        .outfit-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        
        /* 6. Rules Section Styling */
        .rules-section p {
            margin-bottom: 10px; /* Increased separation */
            font-weight: 400; /* Medium weight */
            font-size: 16px;
            line-height: 1.6; /* Even line spacing */
            color: #000000 !important;
        }
        .rules-section strong {
            font-weight: 500; /* Slightly bolder for titles */
        }
        .rules-section {
            background-color: #ffffff !important;
        }
        
        
    """
    
    st.markdown(f"<style>{intro_image_css}{page_fade_css}{color_ui_css}</style>", unsafe_allow_html=True)
    
    # Placeholder for intro music setup
    st.markdown("""
        <audio id="intro-music" src="PLACEHOLDER_FOR_SOFT_MUSIC_CLIP.mp3" preload="auto"></audio>
        <script>
            // MUSIC FADE LOGIC (Conceptual implementation - relies on client-side JS and audio file)
            function playIntroMusic() {
                var music = document.getElementById('intro-music');
                if (music && music.paused) {
                    // Start soft, premium-style background music clip
                    music.volume = 0;
                    music.play();
                    
                    // Fade in (1-2 seconds)
                    var fadeTime = 1500; 
                    var step = 0.05;
                    var delay = (step * fadeTime) / 1;
                    
                    var fadeInInterval = setInterval(function() {
                        if (music.volume < 1) {
                            music.volume = Math.min(1, music.volume + step);
                        } else {
                            clearInterval(fadeInInterval);
                        }
                    }, delay);
                }
            }
            function fadeOutMusic() {
                var music = document.getElementById('intro-music');
                if (music) {
                    // Fade out completely (1 second)
                    var fadeTime = 1000;
                    var step = 0.1;
                    var delay = (step * fadeTime) / 1;
                    
                    var fadeOutInterval = setInterval(function() {
                        if (music.volume > 0) {
                            music.volume = Math.max(0, music.volume - step);
                        } else {
                            music.pause();
                            clearInterval(fadeOutInterval);
                        }
                    }, delay);
                }
            }
        </script>
    """, unsafe_allow_html=True)


# --- Page Functions ---

def intro_video():
    """Displays the new 4-second still intro image and automatically proceeds to login."""
    
    # 1. Intro Sequence: Replace video with 4-second still image
    intro_image_url = INTRO_IMAGE_URL.replace("ibb.co", "i.ibb.co")
    
    intro_class = "intro-screen"
    
    # Trigger music fade-in (Conceptual)
    # st.components.v1.html("<script>playIntroMusic();</script>", height=0)

    # Display the still image in the center (Req 1)
    st.markdown(f"""
    <div class="{intro_class}" id="intro-screen-div">
        <img src="{intro_image_url}" class="intro-image" alt="Style Teller Intro Image">
    </div>
    """, unsafe_allow_html=True)
    
    # Logic to auto-transition after a set time (Req 1)
    MIN_DISPLAY_TIME = 4.0 
    if "intro_start_time" not in st.session_state:
        st.session_state["intro_start_time"] = time.time()
        
    elapsed_time = time.time() - st.session_state["intro_start_time"]
    
    if elapsed_time < MIN_DISPLAY_TIME:
        time.sleep(1) 
        st.rerun() 
    else:
        # 1. Fade-out (1 second) as it transitions into the app.
        st.markdown("<script>document.getElementById('intro-screen-div').classList.add('intro-fade-out');</script>", unsafe_allow_html=True)
        # Fade out music (Conceptual)
        # st.components.v1.html("<script>fadeOutMusic();</script>", height=0)
        time.sleep(1) # Wait for the visual fade-out animation to complete
        
        # Auto-transition to login
        st.session_state["video_played"] = True
        st.session_state["page"] = "login"
        st.rerun()

def login_signup():
    """Login and Signup screen, now with Phone/OTP option."""
    
    # 3. Logo Placement & Animation (Top center, fade-in synced with page)
    logo_url = NEW_LOGO_URL.replace("ibb.co", "i.ibb.co")
    st.markdown(f"""
    <div class='logo-container'>
        <img src="{logo_url}" alt="New Style Teller Logo">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center;'>Style Teller</h1>", unsafe_allow_html=True)
    
    # 4. UI Change: Ensure container is white
    st.markdown("<div class='st-emotion-cache-6o6vcr'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Login or Sign Up</h2>", unsafe_allow_html=True)

    # Use a radio button/tabs for authentication method
    auth_method = st.radio("Choose Login Method", ["Email / Password", "Phone / OTP"], index=0, horizontal=True)

    if auth_method == "Email / Password":
        
        if st.session_state["page"] == "login":
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Login", use_container_width=True, key="email_login_btn"):
                    if email in st.session_state.USER_DB and st.session_state.USER_DB[email]["password"] == password:
                        st.session_state["logged_in"] = True
                        st.session_state["current_user"] = email
                        st.success("Logged in successfully!")
                        
                        # Check onboarding status
                        user_data = st.session_state.USER_DB.get(email, {})
                        user_details = user_data.get("details")
                        if not user_details:
                            st.session_state["page"] = "user_details"
                        elif "styles" not in user_details or not user_details["styles"]:
                            st.session_state["page"] = "choose_style"
                        elif not user_details.get("image_uploaded", False):
                            st.session_state["page"] = "upload_image"
                        else:
                            st.session_state["page"] = "home"
                            st.session_state["show_notification"] = True 
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
            with col2:
                if st.button("Sign Up", use_container_width=True, key="email_signup_btn"):
                    st.session_state["page"] = "signup"
                    st.rerun()
        
        elif st.session_state["page"] == "signup":
            with st.form("signup_form"):
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
                submitted = st.form_submit_button("Create Account")

                if submitted:
                    if email in st.session_state.USER_DB:
                        st.error("Account with this email already exists.")
                    elif password != confirm_password:
                        st.error("Passwords do not match.")
                    else:
                        st.session_state.USER_DB[email] = {"password": password, "details": None, "styles_chosen": False}
                        save_user_db()
                        st.success("Account created successfully! Please log in.")
                        st.session_state["page"] = "login"
                        st.rerun()
        
    elif auth_method == "Phone / OTP":
        # Mock Phone/OTP Logic
        MOCK_OTP = "123456" # Hardcoded mock OTP

        phone_number = st.text_input("Enter Phone Number (e.g., +1234567890)", key="phone_number_input")
        
        if not st.session_state["otp_sent"]:
            if st.button("Send Verification Code", use_container_width=True, key="send_otp_btn"):
                if phone_number and len(phone_number) > 5:
                    st.session_state["mock_phone"] = phone_number
                    st.session_state["otp_sent"] = True
                    # IMPORTANT: In a real app, this would be sent via a service (e.g., Twilio)
                    st.info(f"Mock: Verification code is **{MOCK_OTP}**. Sent to {phone_number}!")
                    st.rerun()
                else:
                    st.error("Please enter a valid phone number.")
        
        if st.session_state["otp_sent"]:
            otp_input = st.text_input("Enter 6-digit Code", max_chars=6, key="otp_input")
            
            if st.button("Verify & Login", use_container_width=True, key="verify_otp_btn"):
                if otp_input == MOCK_OTP:
                    # Treat the phone number as a unique ID for mock persistence
                    mock_email = f"phone_{st.session_state['mock_phone']}"
                    
                    if mock_email not in st.session_state.USER_DB:
                        # Auto-create mock account for phone user
                        st.session_state.USER_DB[mock_email] = {"password": None, "details": None, "styles_chosen": False}
                        save_user_db()

                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = mock_email
                    
                    # Reset OTP state for next login
                    st.session_state["otp_sent"] = False
                    st.session_state["mock_phone"] = None
                    
                    st.success("Verification successful! Logging in...")
                    # Proceed with onboarding/home logic
                    user_data = st.session_state.USER_DB.get(mock_email, {})
                    user_details = user_data.get("details")
                    if not user_details:
                        st.session_state["page"] = "user_details"
                    else:
                        st.session_state["page"] = "home"
                    st.rerun()

                else:
                    st.error("Invalid verification code. Please try again.")


    st.markdown("</div>", unsafe_allow_html=True)
    
def user_details_screen():
    st.title("Tell Us About Yourself")
    with st.form("user_details_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=150, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
        submitted = st.form_submit_button("Continue")
        if submitted:
            st.session_state.USER_DB[st.session_state["current_user"]]["details"] = {
                "name": name,
                "age": age,
                "gender": gender,
                "styles": []
            }
            save_user_db()
            st.session_state["details_provided"] = True
            st.session_state["page"] = "choose_style"
            st.rerun()

def choose_style_screen():
    st.title("Choose Your Style")
    st.markdown("<p style='text-align: center;'>Select at least 3 styles that resonate with you.</p>", unsafe_allow_html=True)
    
    # Updated styles list
    available_styles = [
        "Formal", "Casual", "Streetwear", "Sporty", "Old money",
        "Minimalist", "Hip Hop"
    ]
    
    selected_styles = st.multiselect("Select your styles", available_styles, key="style_multiselect")
    
    if st.button("Save & Continue"):
        if len(selected_styles) >= 3:
            # Handle cases where "details" might be None (e.g., if a user skips steps, though unlikely with current flow)
            user_data = st.session_state.USER_DB[st.session_state["current_user"]]
            if user_data["details"] is None:
                 user_data["details"] = {"styles": selected_styles}
            else:
                 user_data["details"]["styles"] = selected_styles
                 
            save_user_db()
            st.session_state["styles_chosen"] = True
            st.session_state["page"] = "upload_image"
            st.rerun()
        else:
            st.error("Please select at least 3 styles.")
            
def upload_image_screen():
    st.title("Upload Your Image")
    st.markdown("<p>Upload a clear image of yourself so we can create personalized outfit recommendations.</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image of yourself", type=["jpg", "jpeg", "png"])
    
    # 6. Rules Section (on Upload Your Image Page) - With correct styling for black text/font weight
    st.markdown("""
        <div class="rules-section" style="
            background-color: #ffffff; 
            padding: 20px; 
            border-radius: 10px; 
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        ">
        <p style='text-align: center; font-size: 18px; font-weight: 500; margin-bottom: 15px;'>
            Your avatar starts with the right photo<br>
            Here are some quick tips to nail it ✨
        </p>
        <p>
            <strong>• Full Body Shot</strong><br>
            Show your complete outfit from head to toe for accurate style analysis.
        </p>
        <p>
            <strong>• Plain Background</strong><br>
            Use a simple, uncluttered background to help our AI focus on your style.
        </p>
        <p>
            <strong>• Good Lighting</strong><br>
            Natural light works best – avoid shadows and dark areas for clearer photos.
        </p>
        </div>
    """, unsafe_allow_html=True)

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        # Update user details
        user_data = st.session_state.USER_DB[st.session_state["current_user"]]
        if user_data["details"] is None:
             user_data["details"] = {"image_uploaded": True}
        else:
             user_data["details"]["image_uploaded"] = True

        st.session_state["image_uploaded"] = True
        save_user_db()
        st.success("Image uploaded successfully!")
        st.session_state["page"] = "all_set"
        st.rerun()

def all_set_screen():
    st.title("You Are All Set!")
    st.markdown("<p style='text-align: center;'>Your profile is complete. You can now explore your personalized style journey.</p>", unsafe_allow_html=True)
    if st.button("Start Exploring"):
        st.session_state["onboarding_complete"] = True
        st.session_state["page"] = "home"
        st.session_state["show_notification"] = True 
        st.rerun()

def header():
    """Generates the header with navigation options and user info."""
    # 3. Logo Placement & Animation
    logo_url = NEW_LOGO_URL.replace("ibb.co", "i.ibb.co")
    st.markdown(f"""
    <div class='logo-container'>
        <img src="{logo_url}" alt="New Style Teller Logo">
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.button("Home", on_click=lambda: st.session_state.update(page="home"))
    st.sidebar.button("Own Wardrobe", on_click=lambda: st.session_state.update(page="wardrobe"))
    st.sidebar.button("Account", on_click=lambda: st.session_state.update(page="profile"))
    st.sidebar.button("Help", on_click=lambda: st.session_state.update(page="help"))
    st.sidebar.button("Sign Out", on_click=sign_out)

def home_screen():
    st.title("Home")
    
    if st.session_state.get("show_notification", False):
        st.info("Style Teller notification: Your new style recommendations are ready!")
        st.session_state["show_notification"] = False

    user_id = st.session_state["current_user"]
    user_details = st.session_state.USER_DB[user_id].get("details", {})
    
    st.markdown(f"Welcome, **{user_details.get('name', 'Style Enthusiast')}**!")

    st.header("Featured Styles")
    
    if "styles" in user_details and user_details["styles"]:
        # Only show a maximum of 4 styles in the header for clean layout
        styles_to_show = user_details["styles"][:4] 
        style_buttons_container = st.container()
        cols = style_buttons_container.columns(len(styles_to_show))
        for i, style in enumerate(styles_to_show):
            with cols[i]:
                if st.button(style, key=f"style_btn_{i}"):
                    st.session_state["selected_style"] = style
                    st.session_state["page"] = "style_outfits"
                    st.rerun()
    else:
        st.info("You haven't chosen any styles yet. Go to your profile to select some!")

    st.header("Create Your Own Outfit")
    st.button("Start Now", help="Click to create a custom outfit")


def wardrobe_app():
    st.title("Own Wardrobe")
    st.info("Manage your own wardrobe here. This feature is coming soon!")

def show_avatar_outfits():
    st.title("Style Recommendations")
    
    selected_style = st.session_state.get("selected_style", "Formal")
    st.header(f"Outfits for the '{selected_style}' Style")

    # Placeholder outfit generation
    outfit_images = {
        "Formal": [
            "https://placehold.co/300x400/007bff/ffffff?text=Formal+Outfit+1",
            "https://placehold.co/300x400/1e3b68/ffffff?text=Formal+Outfit+2",
            "https://placehold.co/300x400/36454F/ffffff?text=Formal+Outfit+3"
        ],
        "Old money": [
            "https://placehold.co/300x400/8B4513/ffffff?text=Old+Money+Outfit+1",
            "https://placehold.co/300x400/c0c0c0/000000?text=Old+Money+Outfit+2",
            "https://placehold.co/300x400/556B2F/ffffff?text=Old+Money+Outfit+3"
        ],
        "Casual": [
            "https://placehold.co/300x400/FF5733/ffffff?text=Casual+Outfit+1",
            "https://placehold.co/300x400/87CEEB/ffffff?text=Casual+Outfit+2",
            "https://placehold.co/300x400/32CD32/ffffff?text=Casual+Outfit+3"
        ],
        "Streetwear": [
            "https://placehold.co/300x400/1e1e1e/ffffff?text=Streetwear+1",
            "https://placehold.co/300x400/4B0082/ffffff?text=Streetwear+2",
            "https://placehold.co/300x400/FFD700/000000?text=Streetwear+3"
        ]
    }
    
    st.markdown("<div class='outfit-container'>", unsafe_allow_html=True)
    # Use selected style or fallback to Formal
    style_images = outfit_images.get(selected_style) or outfit_images["Formal"]
    
    for i in range(min(3, len(style_images))): # Ensure we don't exceed the image count
        image_url = style_images[i]
        st.markdown(f"""
            <div class='outfit-card'>
                <img src="{image_url}" alt="{selected_style} Outfit {i+1}" />
                <p>Outfit {i+1}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.button("Back to Home", on_click=lambda: st.session_state.update(page="home"))


def profile_screen():
    st.title("My Account")
    user_id = st.session_state["current_user"]
    user_details = st.session_state.USER_DB[user_id].get("details", {})
    
    if user_details:
        st.header("Profile Details")
        st.write(f"**Name:** {user_details.get('name', 'N/A')}")
        st.write(f"**Age:** {user_details.get('age', 'N/A')}")
        st.write(f"**Gender:** {user_details.get('gender', 'N/A')}")
        st.write(f"**Selected Styles:** {', '.join(user_details.get('styles', []))}")

        if st.button("Edit Profile"):
            st.session_state["page"] = "edit_profile"
            st.rerun()
    else:
        st.info("No profile details found. Please complete the onboarding process.")

def edit_profile_screen():
    st.title("Edit Profile")
    user_id = st.session_state["current_user"]
    user_details = st.session_state.USER_DB[user_id].get("details", {})
    
    # Updated styles list
    available_styles = [
        "Formal", "Casual", "Streetwear", "Sporty", "Old money",
        "Minimalist", "Hip Hop"
    ]
    
    with st.form("edit_profile_form"):
        new_name = st.text_input("Name", value=user_details.get("name", ""))
        new_age = st.number_input("Age", min_value=1, max_value=150, value=user_details.get("age", 30))
        gender_options = ["Male", "Female", "Non-binary", "Prefer not to say"]
        current_gender_index = gender_options.index(user_details.get("gender", "Prefer not to say")) if user_details.get("gender") in gender_options else 3
        new_gender = st.selectbox("Gender", gender_options, index=current_gender_index)
        
        new_styles = st.multiselect("Select your styles", available_styles, default=user_details.get("styles", []))
        submitted = st.form_submit_button("Save Changes")
        
        if submitted:
            # Ensure "details" dictionary exists if it was implicitly created (e.g., phone login)
            if st.session_state.USER_DB[user_id]["details"] is None:
                st.session_state.USER_DB[user_id]["details"] = {}
                
            st.session_state.USER_DB[user_id]["details"].update({
                "name": new_name,
                "age": new_age,
                "gender": new_gender,
                "styles": new_styles
            })
            save_user_db()
            st.success("Profile updated successfully!")
            st.session_state["page"] = "profile"
            st.rerun()

def help_screen():
    st.title("Help")
    st.info("For any assistance, please contact support@styleteller.com.")

def sign_out():
    st.session_state.clear()
    st.rerun()

def footer():
    st.sidebar.markdown(
        "<hr style='border: 1px solid #ccc; margin-top: 20px;'>"
        "<div style='text-align: center; color: #888;'>"
        "<small>© 2024 Style Teller</small>"
        "</div>",
        unsafe_allow_html=True
    )

# --- Main App Logic ---

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "page" not in st.session_state:
        st.session_state["page"] = "intro_video"
    if "video_played" not in st.session_state:
        st.session_state["video_played"] = False
    if "USER_DB" not in st.session_state:
        st.session_state.USER_DB = load_user_db()
        
    # NEW state variables for OTP logic
    if "otp_sent" not in st.session_state:
        st.session_state["otp_sent"] = False
    if "mock_phone" not in st.session_state:
        st.session_state["mock_phone"] = None

    set_styles()

    if not st.session_state.get("video_played"):
        # Req 1: Auto-play fullscreen video and auto-transition
        intro_video()
        return

    if not st.session_state["logged_in"]:
        login_signup()
        return

    # User is logged in, display the rest of the app with sidebar
    header()

    # Onboarding flow and page routing
    if st.session_state["page"] == "user_details":
        user_details_screen()
    elif st.session_state["page"] == "choose_style":
        choose_style_screen()
    elif st.session_state["page"] == "upload_image":
        upload_image_screen()
    elif st.session_state["page"] == "all_set":
        all_set_screen()
    elif st.session_state["page"] == "home":
        home_screen()
    elif st.session_state["page"] == "wardrobe":
        wardrobe_app()
    elif st.session_state["page"] == "style_outfits":
        show_avatar_outfits()
    elif st.session_state["page"] == "profile":
        profile_screen()
    elif st.session_state["page"] == "edit_profile":
        edit_profile_screen()
    elif st.session_state["page"] == "help":
        help_screen()
        
    footer()

if __name__ == "__main__":
    main()
