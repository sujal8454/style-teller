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
    """Loads the remembered user's email from the JSON file."""
    if os.path.exists("remembered_user.json"):
        with open("remembered_user.json", "r") as f:
            return json.load(f).get("email")
    return None

# --- Custom Styling ---

def set_styles():
    """Sets the custom CSS for the app, including the new grey background and header text colors."""
    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f0f0;
        }

        .st-emotion-cache-12fmw6v, .st-emotion-cache-12fmw6v:hover, .st-emotion-cache-12fmw6v:active, .st-emotion-cache-12fmw6v:visited, .st-emotion-cache-12fmw6v:focus {
            color: #A52A2A !important;
        }
        
        .st-emotion-cache-1fsy711 > div {
            color: #A52A2A !important;
        }

        .st-emotion-cache-j93igk {
            border-bottom: 2px solid #ccc;
        }
        
        div.st-emotion-cache-6o6vcr {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        /* Adjustments for the new layout and buttons */
        .st-emotion-cache-11r9w7n, .st-emotion-cache-11r9w7n .st-bm {
            width: 100%;
        }

        .st-emotion-cache-13srm2a .st-emotion-cache-7ym5gk {
            margin: 10px 0;
        }

        .st-emotion-cache-17l4y6b {
            flex-direction: column !important;
        }
        
        .st-emotion-cache-1h95u2z {
            text-align: center;
        }
        
        .st-emotion-cache-13l378u {
            text-align: center;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .st-emotion-cache-1kyq27n {
            text-align: center;
        }

        .st-emotion-cache-1v06a5k {
            text-align: center;
        }

        /* Style for the new avatar outfits page */
        .outfit-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }

        .outfit-card {
            background: #fff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }

        .outfit-card img {
            max-width: 100%;
            border-radius: 8px;
        }

        .outfit-card p {
            margin-top: 10px;
            font-weight: bold;
        }
        
        </style>
    """, unsafe_allow_html=True)


# --- Page Functions ---

def intro_video():
    """Displays the intro video screen."""
    st.markdown("<h1 style='text-align: center;'>Welcome to Style Teller</h1>", unsafe_allow_html=True)
    st.video("https://drive.google.com/uc?export=download&id=1XOHOXx16C6Ajiz8vSpQ6ejLj-I-DYoyj", start_time=0)
    
    # Use a button to proceed to the login page
    if st.button("Enter App"):
        st.session_state["video_played"] = True
        st.session_state["page"] = "login"
        st.rerun() # Replaced st.experimental_rerun() with st.rerun()


def login_signup():
    """Login and Signup screen."""
    st.markdown("<h1 style='text-align: center; color: #A52A2A;'>Style Teller</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='st-emotion-cache-6o6vcr'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Login or Sign Up</h2>", unsafe_allow_html=True)

    if st.session_state["page"] == "login":
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True):
                if email in st.session_state.USER_DB and st.session_state.USER_DB[email]["password"] == password:
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = email
                    st.success("Logged in successfully!")
                    
                    # Check onboarding status and set the next page
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
                        st.session_state["show_notification"] = True # Set flag to show notification on home screen
                    st.rerun() # Replaced st.experimental_rerun() with st.rerun()
                else:
                    st.error("Invalid email or password.")
        with col2:
            if st.button("Sign Up", use_container_width=True):
                st.session_state["page"] = "signup"
                st.rerun() # Replaced st.experimental_rerun() with st.rerun()
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
                    st.rerun() # Replaced st.experimental_rerun() with st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    
def user_details_screen():
    st.markdown("<h1 style='text-align: center;'>Tell Us About Yourself</h1>", unsafe_allow_html=True)
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
            st.rerun() # Replaced st.experimental_rerun() with st.rerun()

def choose_style_screen():
    st.markdown("<h1 style='text-align: center;'>Choose Your Style</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Select at least 3 styles that resonate with you.</p>", unsafe_allow_html=True)
    
    available_styles = [
        "Formal", "Casual", "Streetwear", "Boho", "Sporty", "Old money",
        "Minimalist", "Vintage", "Preppy", "Gothic", "Punk", "Hip Hop"
    ]
    
    selected_styles = st.multiselect("Select your styles", available_styles, key="style_multiselect")
    
    if st.button("Save & Continue"):
        if len(selected_styles) >= 3:
            st.session_state.USER_DB[st.session_state["current_user"]]["details"]["styles"] = selected_styles
            save_user_db()
            st.session_state["styles_chosen"] = True
            st.session_state["page"] = "upload_image"
            st.rerun() # Replaced st.experimental_rerun() with st.rerun()
        else:
            st.error("Please select at least 3 styles.")
            
def upload_image_screen():
    st.markdown("<h1 style='text-align: center;'>Upload Your Image</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload an image of yourself", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.session_state.USER_DB[st.session_state["current_user"]]["details"]["image_uploaded"] = True
        st.session_state["image_uploaded"] = True
        save_user_db()
        st.success("Image uploaded successfully!")
        st.session_state["page"] = "all_set"
        st.rerun() # Replaced st.experimental_rerun() with st.rerun()

def all_set_screen():
    st.markdown("<h1 style='text-align: center;'>You Are All Set!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Your profile is complete. You can now explore your personalized style journey.</p>", unsafe_allow_html=True)
    if st.button("Start Exploring"):
        st.session_state["onboarding_complete"] = True
        st.session_state["page"] = "home"
        st.session_state["show_notification"] = True # Set flag to show notification on home screen
        st.rerun() # Replaced st.experimental_rerun() with st.rerun()

def header():
    """Generates the header with navigation options and user info."""
    st.sidebar.markdown(
        "<div style='background-color: #f0f0f0; padding: 10px; border-radius: 10px;'>"
        "<h2 style='text-align: center; color: #A52A2A;'>Style Teller</h2>"
        "<hr style='border: 1px solid #ccc;'>"
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
    user_details = st.session_state.USER_DB[user_id]["details"]
    st.markdown(f"Welcome, **{user_details['name']}**!")

    # Featured Styles section
    st.header("Featured Styles")
    
    # Check if the user has chosen styles
    if "styles" in user_details and user_details["styles"]:
        style_buttons_container = st.container()
        cols = style_buttons_container.columns(len(user_details["styles"]))
        for i, style in enumerate(user_details["styles"]):
            with cols[i]:
                if st.button(style):
                    st.session_state["selected_style"] = style
                    st.session_state["page"] = "style_outfits"
                    st.rerun() # Replaced st.experimental_rerun() with st.rerun()
    else:
        st.info("You haven't chosen any styles yet. Go to your profile to select some!")

    # Create Your Own Outfit
    st.header("Create Your Own Outfit")
    st.button("Start Now", help="Click to create a custom outfit")


def wardrobe_app():
    st.title("Own Wardrobe")
    st.info("Manage your own wardrobe here. This feature is coming soon!")

def show_avatar_outfits():
    st.title("Style Recommendations")
    
    selected_style = st.session_state.get("selected_style", "Formal")
    st.header(f"Outfits for the '{selected_style}' Style")

    # This is a placeholder for outfit generation. In a real app, this would use an LLM or image model.
    # For now, we will show some example outfits.
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
    for i in range(3):
        image_url = outfit_images.get(selected_style, outfit_images["Formal"])[i]
        st.markdown(f"""
            <div class='outfit-card'>
                <img src="{image_url}" alt="{selected_style} Outfit {i+1}" />
                <p>Outfit {i+1}</p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.button("Back to Home", on_click=lambda: st.session_state.update(page="home"))


def outfit_results():
    """This page no longer contains outfit creation options and is only for displaying outfits."""
    show_avatar_outfits()

def profile_screen():
    st.title("My Account")
    user_id = st.session_state["current_user"]
    user_details = st.session_state.USER_DB[user_id]["details"]
    
    if user_details:
        st.header("Profile Details")
        st.write(f"**Name:** {user_details['name']}")
        st.write(f"**Age:** {user_details['age']}")
        st.write(f"**Gender:** {user_details['gender']}")
        st.write(f"**Selected Styles:** {', '.join(user_details.get('styles', []))}")

        if st.button("Edit Profile"):
            st.session_state["page"] = "edit_profile"
            st.rerun() # Replaced st.experimental_rerun() with st.rerun()
    else:
        st.info("No profile details found. Please complete the onboarding process.")

def edit_profile_screen():
    st.title("Edit Profile")
    user_id = st.session_state["current_user"]
    user_details = st.session_state.USER_DB[user_id]["details"]
    
    with st.form("edit_profile_form"):
        new_name = st.text_input("Name", value=user_details.get("name", ""))
        new_age = st.number_input("Age", min_value=1, max_value=150, value=user_details.get("age", 30))
        new_gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"], index=["Male", "Female", "Non-binary", "Prefer not to say"].index(user_details.get("gender", "Prefer not to say")))
        available_styles = [
            "Formal", "Casual", "Streetwear", "Boho", "Sporty", "Old money",
            "Minimalist", "Vintage", "Preppy", "Gothic", "Punk", "Hip Hop"
        ]
        new_styles = st.multiselect("Select your styles", available_styles, default=user_details.get("styles", []))
        submitted = st.form_submit_button("Save Changes")
        
        if submitted:
            st.session_state.USER_DB[user_id]["details"].update({
                "name": new_name,
                "age": new_age,
                "gender": new_gender,
                "styles": new_styles
            })
            save_user_db()
            st.success("Profile updated successfully!")
            st.session_state["page"] = "profile"
            st.rerun() # Replaced st.experimental_rerun() with st.rerun()

def help_screen():
    st.title("Help")
    st.info("For any assistance, please contact support@styleteller.com.")

def sign_out():
    st.session_state["logged_in"] = False
    st.session_state["current_user"] = None
    st.session_state["page"] = "login"
    st.session_state["video_played"] = False
    st.session_state.clear()
    st.rerun() # Replaced st.experimental_rerun() with st.rerun()

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

    set_styles()

    if not st.session_state.get("video_played"):
        intro_video()
        return

    if not st.session_state["logged_in"]:
        login_signup()
        return

    # User is logged in, display the rest of the app with sidebar
    header()

    # Onboarding flow for new users
    user_id = st.session_state["current_user"]
    user_data = st.session_state.USER_DB.get(user_id, {})
    user_details = user_data.get("details")

    # This part of the code determines the page to show based on the 'page' state variable.
    # The login_signup function now sets this variable correctly.
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
