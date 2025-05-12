import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json
import os
import time
import base64

def save_user_db():
    with open("user_db.json", "w") as f:
        json.dump(st.session_state.USER_DB, f)

def load_user_db():
    if os.path.exists("user_db.json"):
        with open("user_db.json", "r") as f:
            return json.load(f)
    return {
        "demo@example.com": "password123",
        "alice@example.com": "stylequeen",
        "bob@example.com": "fashionking"
    }

def generate_ai_image(face_image, outfit_type, category):
    url = f"https://placehold.co/600x800.png?text={outfit_type}+{category}"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def header():
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

def login_signup():
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

    auth_mode = st.radio("Select an option", ["Login", "Sign Up"], horizontal=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
 
    remember_me = st.checkbox("Remember me")

    if auth_mode == "Login":
        if st.button("Login"):
            if email in st.session_state.USER_DB and st.session_state.USER_DB[email] == password:
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = email
       
                if remember_me:
                    st.session_state["remembered_email"] = email
                    st.session_state["remembered_password"] = password
             
                st.session_state["show_welcome"] = True
                st.session_state["welcome_time"] = time.time()
                st.rerun()

            else:
                st.error("Invalid email or password.")
    else:
        password_confirm = st.text_input("Confirm Password", type="password")
        
        if st.button("Sign Up"):
            if email in st.session_state.USER_DB:
                st.error("Email already registered.")
            elif not "@" in email or not "." in email:
                st.error("Please enter a valid email address.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            elif password != password_confirm:
                st.error("Passwords do not match.")
            else:
                st.session_state.USER_DB[email] = password
                save_user_db()  
              
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = email
         
                if remember_me:
                    st.session_state["remembered_email"] = email
                    st.session_state["remembered_password"] = password
         
                st.session_state["show_welcome"] = True
                st.session_state["welcome_time"] = time.time()
               st.rerun()

def home_screen():
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
    
    user_name = st.session_state["current_user"].split('@')[0]
   
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
    user_email = st.session_state["current_user"]
    user_name = user_email.split('@')[0]

    st.subheader("Account Information")
    st.markdown(f"<div class='text-with-bg'><strong>Email:</strong> {user_email}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='text-with-bg'><strong>User Name:</strong> {user_name}</div>", unsafe_allow_html=True)
    
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
            del st.session_state["remembered_password"]
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
    
    st.subheader("How to Use Style Teller")
    
    with st.expander("Creating an Outfit", expanded=True):
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
    st.set_page_config(page_title="Style Teller", layout="centered", page_icon="🧥")
    
    if "USER_DB" not in st.session_state:
        st.session_state.USER_DB = load_user_db()
        
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if "page" not in st.session_state:
        st.session_state["page"] = "home"

    component_value = st.session_state.get("component_value")
    if component_value == "home":
        st.session_state["page"] = "home"
    elif component_value == "profile":
        st.session_state["page"] = "profile"
    elif component_value == "settings":
        st.session_state["page"] = "settings"
    elif component_value == "logout":
        st.session_state["logged_in"] = False
        if "remembered_email" in st.session_state:
            del st.session_state["remembered_email"]
            del st.session_state["remembered_password"]
    
    if not st.session_state["logged_in"] and "remembered_email" in st.session_state:
        email = st.session_state["remembered_email"]
        password = st.session_state["remembered_password"]
        if email in st.session_state.USER_DB and st.session_state.USER_DB[email] == password:
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = email

    if not st.session_state["logged_in"]:
        login_signup()
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

if __name__ == "__main__":
    main()
