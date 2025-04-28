import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json
import os

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

def login_signup():
    st.title("Style Teller")

    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-attachment: fixed;
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
                
                st.success(f"Welcome back, {email.split('@')[0]}!")
                st.balloons()  # Celebratory animation
                st.experimental_rerun()
            else:
                st.error("Invalid email or password.")
    else:
        if st.button("Sign Up"):
            if email in st.session_state.USER_DB:
                st.error("Email already registered.")
            elif not "@" in email or not "." in email:
                st.error("Please enter a valid email address.")
            else:
                st.session_state.USER_DB[email] = password
                save_user_db()  # Save updated user database
                st.success("Account created! You can now log in.")

def wardrobe_app():
    st.title("🧥 Style Teller Wardrobe")
    
    user_name = st.session_state["current_user"].split('@')[0]
    st.sidebar.markdown(f"""
    <div style="background-color:#4CAF50; padding:10px; border-radius:5px; margin-bottom:20px;">
        <h3 style="color:white; margin:0;">Welcome back, {user_name}!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("Welcome to your AI-powered virtual wardrobe!")

    st.markdown("""
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1558769132-cb1aea458c5e?auto=format&fit=crop&w=1350&q=80');
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.expander("📸 Upload Your Face"):
        face_image = st.file_uploader("Upload a clear face image", type=["jpg", "png"])
        if face_image:
            img = Image.open(face_image)
            st.image(img, caption="Your uploaded image", width=200)

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
    outfit_type = st.selectbox("Style Type", ["Formal", "Old Money", "College", "School", "Streetwear"])
    occasion = st.text_input("Occasion (e.g., Party, Office, Casual)")

    if st.button("Generate Outfits"):
        if face_image:
            st.success("Generating AI outfit suggestions...")
            categories = ["Topwear", "Bottomwear", "Full Outfit", "Accessories"]
            
            st.subheader("Virtual Try-On")
            st.image("https://placehold.co/800x1000.png?text=AI+Generated+Face+With+Outfit", 
                    caption="AI-generated image of you in the outfit", use_column_width=True)
            
            st.subheader("Individual Items")
            for cat in categories:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown(f"### {cat}")
                with col2:
                    img = generate_ai_image(face_image, outfit_type, cat)
                    st.image(img, caption=f"{cat} Look", use_column_width=True)
        else:
            st.warning("Please upload your face photo.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        if "remembered_email" in st.session_state:
            del st.session_state["remembered_email"]
            del st.session_state["remembered_password"]
        st.experimental_rerun()

def main():
    st.set_page_config(page_title="Style Teller", layout="centered", page_icon="🧥")
    
    if "USER_DB" not in st.session_state:
        st.session_state.USER_DB = load_user_db()
        
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    
    if not st.session_state["logged_in"] and "remembered_email" in st.session_state:
        email = st.session_state["remembered_email"]
        password = st.session_state["remembered_password"]
        if email in st.session_state.USER_DB and st.session_state.USER_DB[email] == password:
            st.session_state["logged_in"] = True
            st.session_state["current_user"] = email

    if not st.session_state["logged_in"]:
        login_signup()
    else:
        wardrobe_app()

if __name__ == "__main__":
    main()
