import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json
import os
import time
import base64
import random

# --- Database and File Handling Functions ---

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

# --- Custom Styling (Includes UI Fixes and Fullscreen Video CSS) ---

def set_styles():
    """Sets the custom CSS for the app, ensuring light background, black text, and fullscreen video."""
    
    # NEW: 5. Background Image and Overlay
    # Placeholder URL for the background image. Replace with your actual hosted image URL if you have one.
    # Using a high-quality, fashion-appropriate image URL to match the premium aesthetic.
    BG_IMAGE_URL = "https://images.unsplash.com/photo-1558239044-6a0c0e705469?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" 
    
    st.markdown(f"""
        <style>
        
        /* --------------------------------- ANIMATIONS --------------------------------- */

        /* 2. Page-Load Transition: Gentle fade-in (1 second) for the entire content */
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}

        /* 1. Intro Video Fade-In (1.5 seconds) */
        @keyframes videoFadeIn {{
            from {{ opacity: 0; }} /* Start at 0 opacity */
            to {{ opacity: 1; }}
        }}
        
        /* 3. Logo Fade-In (Synchronized with page fade-in) */
        @keyframes logoFadeIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* --------------------------------- GLOBAL STYLES --------------------------------- */

        /* 5. Background Image, Cover, Center, Repeat */
        .stApp {{
            background-color: #ffffff; /* Fallback */
            background-image: url("{BG_IMAGE_URL}");
            background-size: cover; /* Required property */
            background-position: center; /* Required property */
            background-repeat: no-repeat; /* Required property */
            
            /* Apply general page fade-in (2. Page-Load Transition) */
            animation: fadeIn 1s ease-in-out forwards; /* 'forwards' ensures it stays visible */
            position: relative; 
        }}
        
        /* 5. Soft white overlay (15% opacity) */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(255, 255, 255, 0.15); /* 15% opacity white overlay */
            z-index: 0; 
        }}

        /* Ensure all app content is above the overlay */
        div[data-testid="stAppViewContainer"], 
        div[data-testid="stSidebar"], 
        div[data-testid="stHeader"] {{
            z-index: 1;
            background: transparent !important; 
        }}
        
        /* 4. Color & UI Updates: Ensure ALL text is BLACK (#000000) for readability on white/light background */
        div, span, p, a, label, h1, h2, h3, h4, 
        .stApp, 
        div[data-testid="stAppViewContainer"] *,
        div[data-baseweb="form-control"] label
        {{
            color: #000000 !important;
            font-family: sans-serif; /* Clean, modern font */
            font-weight: 400; /* Medium weight, not bold (Req 6) */
        }}
        
        /* Sidebar/Dark Element Text (Keep text white on the default dark sidebar) */
        div[data-testid="stSidebar"] *, 
        div[data-testid="stSidebarContent"] button 
        {{
            color: #ffffff !important;
        }}
        
        /* --- 4. CRITICAL INPUT FIELD & BLACK BOX OVERRIDE (Fix Black Boxes to White: #FFFFFF) --- */

        /* Target the actual input element */
        div[data-baseweb="input"] input,
        div[data-baseweb="input"] textarea,
        input[type="text"], 
        input[type="password"],
        input[type="number"],
        textarea {{
            background-color: #ffffff !important; /* Force the field itself to white */
            color: #000000 !important; /* Force text to black */
            border: 1px solid #000000 !important; 
            -webkit-appearance: none; 
            appearance: none;
        }}
        
        /* Ensure the input containers are also white */
        div[data-testid="stTextInput"] > div > div, 
        div[data-testid="stNumberInput"] > div > div,
        div[data-testid="stSelectbox"] > div,
        div[data-baseweb="input"],
        div.st-emotion-cache-1fcpj1c, /* Generic Streamlit input wrapper */
        div.st-emotion-cache-16j94j4, /* Another common input wrapper class */
        div.st-emotion-cache-6o6vcr, /* General block container/box */
        div[data-testid="stForm"], /* Form container */
        div[data-testid="stAlert"], /* Alert/info boxes */
        div[data-testid="stVerticalBlock"] > div:first-child:not([data-testid="stSidebarContent"]),
        div[data-testid="stVerticalBlock"] > div:nth-child(2)
        {{
            background-color: #ffffff !important; /* Pure White background (#FFFFFF) */
            border: 1px solid #000000 !important; /* Black border for definition */
            box-shadow: 0 2px 5px rgba(0,0,0,0.05); /* Soft shadow for premium feel */
        }}
        
        /* --- 4. BUTTON STYLING OVERRIDE (Fix Black Buttons to White) --- */

        div[data-testid*="stButton"] > button {{
            background-color: #ffffff !important; /* Pure White background */
            color: #000000 !important; /* Black text */
            border: 1px solid #000000 !important; /* Black border for distinction */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }}
        
        div[data-testid*="stButton"] > button:hover {{
            color: #000000 !important; 
            border: 1px solid #000000 !important; 
            background-color: #f0f0f0 !important; 
        }}
        
        /* --- 3. Logo Placement & Animation --- */
        .logo-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            padding-top: 20px;
            padding-bottom: 20px;
            margin-bottom: -15px; 
            animation: logoFadeIn 1s ease-out 0s forwards; /* Synchronized Fade-In */
            opacity: 0; /* Start hidden for animation */
            z-index: 2;
        }}

        .app-logo {{
            max-width: 150px; /* Proportionate size */
            height: auto;
            border-radius: 0;
        }}

        /* --- 1. Intro Video Fullscreen Fix & Animation --- */
        
        /* Remove any dark overlay by setting the video container background to black */
        .video-active div[data-testid="stAppViewContainer"] {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 9999;
            background-color: #000000 !important; 
            padding: 0 !important;
            margin: 0 !important;
        }}
        
        /* Apply smooth fade-in animation to the video element */
        .video-active div[data-testid="stVerticalBlock"] {{
            animation: videoFadeIn 1.5s ease-in-out forwards; /* Smooth fade-in (1-2 seconds) */
        }}
        
        /* Fix the video to cover the screen smoothly */
        .video-active video {{
             width: 100vw !important;
             height: 100vh !important;
             object-fit: cover !important; 
        }}
        
        /* Hide sidebar while video is active */
        .video-active div[data-testid="stSidebar"] {{
            display: none !important;
        }}

        </style>
        <script>
        // Use Javascript to toggle a class on the body to control video fullscreen
        function setVideoMode(isActive) {{
            if (isActive) {{
                document.body.classList.add('video-active');
            }} else {{
                // Remove the class when done to return to normal
                document.body.classList.remove('video-active');
            }}
        }}
        </script>
    """, unsafe_allow_html=True)


def display_logo():
    """3. Displays the high-res, center-aligned logo with fade-in animation."""
    # Placeholder for the uploaded logo data (base64)
    logo_b64 = st.session_state.get("logo_src")

    if logo_b64:
        st.markdown(f"""
            <div class='logo-container'>
                <img src="data:image/png;base64,{logo_b64}" class="app-logo" alt="Style Teller Logo" />
            </div>
        """, unsafe_allow_html=True)

# --- Page Functions ---

def intro_video():
    """Displays the intro video screen and automatically proceeds to login."""
    # 1. Fix intro video to play smoothly, remove black overlay, and add fade-in
    st.components.v1.html("<script>setVideoMode(true);</script>", height=0)
    
    # Using a publicly accessible MP4 for reliable playback
    VIDEO_URL = "https://static.videezy.com/system/resources/previews/000/054/104/original/10_Second_Countdown.mp4"
    st.video(VIDEO_URL, start_time=0)
    
    # Logic to auto-transition after a set time (simulates video completion)
    MIN_DISPLAY_TIME = 4.0
    if "video_start_time" not in st.session_state:
        st.session_state["video_start_time"] = time.time()

    elapsed_time = time.time() - st.session_state["video_start_time"]
    
    if elapsed_time < MIN_DISPLAY_TIME:
        # Show progress bar and countdown text
        progress_text = f"Starting app... {int(MIN_DISPLAY_TIME - elapsed_time) + 1}s"
        # Ensure progress bar text is black (or white in video mode)
        st.progress(elapsed_time / MIN_DISPLAY_TIME, text=progress_text)
        time.sleep(1) 
        st.rerun() 
    else:
        # Auto-transition to login
        st.session_state["video_played"] = True
        st.session_state["page"] = "login"
        st.rerun()

def login_signup():
    """Login and Signup screen."""
    # Run JS to deactivate fullscreen mode CSS
    st.components.v1.html("<script>setVideoMode(false);</script>", height=0)
    
    st.markdown("<h1 style='text-align: center;'>Style Teller</h1>", unsafe_allow_html=True)
    
    # Use the custom white box styling
    st.markdown("<div class='st-emotion-cache-6o6vcr'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Login or Sign Up</h2>", unsafe_allow_html=True)

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
        MOCK_OTP = "123456" 

        phone_number = st.text_input("Enter Phone Number (e.g., +1234567890)", key="phone_number_input")
        
        if not st.session_state["otp_sent"]:
            if st.button("Send Verification Code", use_container_width=True, key="send_otp_btn"):
                if phone_number and len(phone_number) > 5:
                    st.session_state["mock_phone"] = phone_number
                    st.session_state["otp_sent"] = True
                    st.info(f"Mock: Verification code is **{MOCK_OTP}**. Sent to {phone_number}!")
                    st.rerun()
                else:
                    st.error("Please enter a valid phone number.")
        
        if st.session_state["otp_sent"]:
            otp_input = st.text_input("Enter 6-digit Code", max_chars=6, key="otp_input")
            
            if st.button("Verify & Login", use_container_width=True, key="verify_otp_btn"):
                if otp_input == MOCK_OTP:
                    mock_email = f"phone_{st.session_state['mock_phone']}"
                    
                    if mock_email not in st.session_state.USER_DB:
                        st.session_state.USER_DB[mock_email] = {"password": None, "details": None, "styles_chosen": False}
                        save_user_db()

                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = mock_email
                    
                    st.session_state["otp_sent"] = False
                    st.session_state["mock_phone"] = None
                    
                    st.success("Verification successful! Logging in...")
                    
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
            user_data = st.session_state.USER_DB[st.session_state["current_user"]]
            if user_data.get("details") is None:
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
    
    # 6. Rules Section Re-added with required styling (Black text, clean, elegant, modern font, proper spacing)
    st.markdown("""
        <div style="margin-top: 30px; padding: 20px; border: 1px solid #000000; border-radius: 5px; background-color: #ffffff;">
            <p style="font-weight: 500; font-size: 1.1em; color: #000000; margin-bottom: 15px; font-family: sans-serif;">
                Your avatar starts with the right photo<br>
                Here are some quick tips to nail it ✨
            </p>
            <ul style="list-style-type: none; padding-left: 0; line-height: 1.5; font-family: sans-serif;">
                <li style="color: #000000; margin-bottom: 12px;">
                    <strong style="font-weight: 500;">• Full Body Shot</strong><br>
                    <span style="font-weight: 300; color: #000000; font-size: 0.95em;">Show your complete outfit from head to toe for accurate style analysis.</span>
                </li>
                <li style="color: #000000; margin-bottom: 12px;">
                    <strong style="font-weight: 500;">• Plain Background</strong><br>
                    <span style="font-weight: 300; color: #000000; font-size: 0.95em;">Use a simple, uncluttered background to help our AI focus on your style.</span>
                </li>
                <li style="color: #000000;">
                    <strong style="font-weight: 500;">• Good Lighting</strong><br>
                    <span style="font-weight: 300; color: #000000; font-size: 0.95em;">Natural light works best – avoid shadows and dark areas for clearer photos.</span>
                </li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        # Update user details
        user_data = st.session_state.USER_DB[st.session_state["current_user"]]
        if user_data.get("details") is None:
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
    # Custom sidebar styling with white background/black text exception handled in set_styles
    st.sidebar.markdown(
        "<div style='padding: 10px 0 10px 0;'>"
        "<h2 style='text-align: center; color: #ffffff; margin-bottom: 5px;'>Style Teller</h2>" 
        "<hr style='border: 1px solid #ffffff33; margin-top: 5px; margin-bottom: 10px;'>"
        "</div>",
        unsafe_allow_html=True
    )
    
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
    style_images = outfit_images.get(selected_style) or outfit_images["Formal"]
    
    for i in range(min(3, len(style_images))):
        image_url = style_images[i]
        # Use a div for outfit card and ensure it respects the white box/black text aesthetic
        st.markdown(f"""
            <div class='outfit-card' style="background-color: #ffffff; border: 1px solid #000000; padding: 10px;">
                <img src="{image_url}" alt="{selected_style} Outfit {i+1}" style="border-radius: 8px;" />
                <p style="color: #000000;">Outfit {i+1}</p>
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
            if st.session_state.USER_DB[user_id].get("details") is None:
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
        "<hr style='border: 1px solid #ffffff33; margin-top: 20px;'>"
        "<div style='text-align: center; color: #ccc;'>"
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
        
    if "otp_sent" not in st.session_state:
        st.session_state["otp_sent"] = False
    if "mock_phone" not in st.session_state:
        st.session_state["mock_phone"] = None
        
    # 3. Logo Source Placeholder (Using a simple base64 encoded image to simulate the uploaded logo)
    if "logo_src" not in st.session_state:
         # Placeholder for a simple Style Teller logo image
         st.session_state["logo_src"] = "iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAYAAAA8AX2jAAAACXBIWXMAAAsTAAALEwEAmpwYAAABHklEQVR4nO3WsQ0AIAwEsH/ptJvR5gN0V8hNzsUAAAAAAAAA7/1V/N/kL37tT71U6A8BAAAAAAAAAAAgGWAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgMmAyYDJgAAAAAAbn8F+L9PvwGj5gEwAAAAAElFTkSuQmCC"

    # Apply all required custom styles and animations
    set_styles()
    
    # 1. Intro Video logic
    if not st.session_state.get("video_played"):
        intro_video()
        return

    # 3. Display Logo for all screens after the video
    display_logo()

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
