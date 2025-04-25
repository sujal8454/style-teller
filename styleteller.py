import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def generate_ai_image(face_image, outfit_type, category):
    url = f"https://placehold.co/600x800?text={outfit_type}+{category}"
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

if "USER_DB" not in st.session_state:
    st.session_state.USER_DB = {
        "demo": "password123",
        "alice": "stylequeen",
        "bob": "fashionking"
    }

def login_signup():
    st.title("Style Teller")

    auth_mode = st.radio("Select an option", ["Login", "Sign Up"], horizontal=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if auth_mode == "Login":
        if st.button("Login"):
            if username in st.session_state.USER_DB and st.session_state.USER_DB[username] == password:
                st.success("Logged in successfully!")
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = username
            else:
                st.error("Invalid username or password.")
    else:
        if st.button("Sign Up"):
            if username in st.session_state.USER_DB:
                st.error("Username already exists.")
            else:
                st.session_state.USER_DB[username] = password
                st.success("Account created! You can now log in.")

def wardrobe_app():
    st.title("🧥 Style Teller Wardrobe")
    st.markdown("Welcome to your AI-powered virtual wardrobe!")

    with st.expander("📸 Upload Your Face"):
        face_image = st.file_uploader("Upload a clear face image", type=["jpg", "png"])

    body_type = st.selectbox("Choose Your Body Type", ["Slim", "Athletic", "Curvy", "Plus-size"])
    gender = st.radio("Select Gender", ["Male", "Female", "Other"])
    body_color = st.color_picker("Choose Your Skin Tone", "#f1c27d")
    color_choice = st.text_input("Optional: Favorite color palette")
    outfit_type = st.selectbox("Style Type", ["Formal", "Old Money", "College", "School", "Streetwear"])
    occasion = st.text_input("Occasion (e.g., Party, Office, Casual)")

    if st.button("Generate Outfits"):
        if face_image:
            st.success("Generating AI outfit suggestions...")
            categories = ["Topwear", "Bottomwear", "Full Outfit", "Accessories"]
            for cat in categories:
                st.subheader(f"🧷 {cat}")
                img = generate_ai_image(face_image, outfit_type, cat)
                st.image(img, caption=f"{cat} Look", use_column_width=True)
        else:
            st.warning("Please upload your face photo.")

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.experimental_rerun()

def main():
    st.set_page_config(page_title="Style Teller", layout="centered", page_icon="🧥")
    bg_img = """
    <style>
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1602810318383-0e5b5c5f6b87');
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login_signup()
    else:
        wardrobe_app()

if __name__ == "__main__":
    main()
