# --- START: StyleTeller UI Enhancements (intro, theme, logo, background, rules) ---
import streamlit as st
from streamlit.components.v1 import html as components_html

_intro_html = r"""
<style>
/* Page fade-in */
.stApp { opacity: 0; transition: opacity 1s ease; --stapp-opacity: 1; }

/* Custom logo header */
#custom-logo-header {
  position: relative;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 8px;
  z-index: 1001;
  pointer-events: none;
  opacity: 0;
  transition: opacity 1s ease;
}
#custom-logo-header img { max-height: 72px; width: auto; object-fit: contain; }

/* Intro overlay full-screen */
#intro-overlay {
  position: fixed; inset: 0; display: flex; align-items: center; justify-content: center;
  z-index: 10000; background: rgba(255,255,255,1);
}
#intro-overlay img { max-width: 80vw; max-height: 80vh; width: auto; height: auto; border-radius: 6px; box-shadow: 0 10px 30px rgba(0,0,0,0.08); opacity: 0; transition: opacity 1.5s ease; }

/* Background image & white overlay */
html, body { height: 100%; }
body {
  background-image: url('https://ibb.co/gMDjN4Mt');
  background-size: cover; background-position: center; background-repeat: no-repeat !important;
  background-color: #ffffff;
}

/* white overlay on background - placed behind app content */
#background-white-overlay {
  position: fixed; inset: 0; z-index: -9998; pointer-events: none;
  background-color: rgba(255,255,255,0.12);
  width: 100%; height: 100%;
}

/* Force white boxes & black text for common containers */
.stApp .block-container,
.stApp .element-container,
.stApp .stButton,
.stApp .main,
.stApp .stMarkdown,
.stApp .stTextInput,
.stApp .stFileUploader,
.stApp .stSidebar {
  background-color: #FFFFFF !important;
  color: #000000 !important;
}

/* Also override inline black backgrounds if present */
*[style*="background-color: rgb(0, 0, 0)"]{ background-color: #FFFFFF !important; color: #000000 !important; }
*[style*="background:#000"], *[style*="background: #000"], *[style*="background-color:#000"]{ background-color: #FFFFFF !important; color: #000000 !important; }

/* Rules block */
.custom-rules { font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial; color: #000000; font-weight: 500; line-height: 1.5; margin-top: 12px; }
.custom-rules .title { font-size: 16px; margin-bottom: 8px; }
.custom-rules ul { margin-top: 8px; padding-left: 18px; }
.custom-rules li { margin-bottom: 10px; }

/* Ensure inputs and textareas keep black text on white backgrounds */
input, textarea, select { color: #000000 !important; background-color: #FFFFFF !important; }

</style>

<div id="intro-overlay" aria-hidden="true">
  <img id="intro-image" src="https://ibb.co/B5qxJWW8" alt="Intro" />
  <audio id="intro-audio" src="" preload="auto"></audio>
</div>

<div id="background-white-overlay"></div>

<script>
(function(){
  const AUDIO_ENABLED = true; // attempt to play; browsers may block autoplay

  const audio = document.getElementById('intro-audio');
  // NOTE: Using an external audio URL may be blocked; left empty so browser fallback is graceful.
  // If you prefer a bundled audio clip, replace audio.src with a valid URL or base64 data URI.
  audio.loop = false;
  audio.volume = 0.0;

  const overlay = document.getElementById('intro-overlay');
  const img = document.getElementById('intro-image');

  // Small delay to let component mount, then fade in image and attempt audio
  setTimeout(()=>{ 
    try{ img.style.opacity = 1; }catch(e){}
    if(AUDIO_ENABLED){
      try{ 
        const playPromise = audio.play();
        if(playPromise !== undefined){
          playPromise.then(()=>{ fadeAudioIn(audio,1500); }).catch(()=>{/* autoplay blocked */});
        }
      } catch(e){}
    }
  }, 60);

  // After 4 seconds total, fade out overlay over 1s, fade audio out, then remove overlay and show app
  setTimeout(()=> {
    overlay.style.transition = 'opacity 1s ease';
    overlay.style.opacity = 0;
    fadeAudioOut(audio,1000);
    setTimeout(()=>{ overlay.remove(); showMainApp(); }, 1000);
  }, 4000);

  function showMainApp(){
    const app = document.querySelector('.stApp');
    if(app){ app.style.opacity = 1; }
    // insert custom logo header if not exists
    if(!document.getElementById('custom-logo-header')){
      const header = document.createElement('div');
      header.id = 'custom-logo-header';
      header.innerHTML = '<img src="https://i.ibb.co/3YMDZQVn"alt="Logo" id="custom-logo-img" />';
      document.body.insertBefore(header, document.body.firstChild);
      setTimeout(()=>{ header.style.opacity = 1; }, 50);
    } else {
      document.getElementById('custom-logo-header').style.opacity = 1;
    }

    // Inject rules block under the first file input (upload)
    setTimeout(()=> {
      try {
        const fileInput = document.querySelector('input[type=file]');
        if(fileInput){
          let container = fileInput.closest('div');
          if(!container){ container = fileInput.parentElement; }
          const rules = document.createElement('div');
          rules.className = 'custom-rules';
          rules.innerHTML = `
            <div class="title"><strong>Your avatar starts with the right photo</strong><br><small>Here are some quick tips to nail it ✨</small></div>
            <ul>
              <li><strong>Full Body Shot</strong><div>Show your complete outfit from head to toe for accurate style analysis.</div></li>
              <li><strong>Plain Background</strong><div>Use a simple, uncluttered background to help our AI focus on your style.</div></li>
              <li><strong>Good Lighting</strong><div>Natural light works best – avoid shadows and dark areas for clearer photos.</div></li>
            </ul>
          `;
          if(container.nextSibling){ container.parentNode.insertBefore(rules, container.nextSibling); } else { container.parentNode.appendChild(rules); }
        }
      } catch(e){}
    }, 200);
  }

  function fadeAudioIn(audio, duration){
    if(!audio) return;
    let step = 50;
    let steps = Math.max(1, Math.floor(duration/step));
    let inc = 1.0/steps;
    audio.volume = 0;
    let i=0;
    let t = setInterval(()=>{ i++; audio.volume = Math.min(1, audio.volume + inc); if(i>=steps){ clearInterval(t); } }, step);
  }
  function fadeAudioOut(audio, duration){
    if(!audio) return;
    let step = 50;
    let steps = Math.max(1, Math.floor(duration/step));
    let dec = (audio.volume||1)/steps;
    let i=0;
    let t = setInterval(()=>{ i++; audio.volume = Math.max(0, audio.volume - dec); if(i>=steps){ audio.pause(); clearInterval(t); } }, step);
  }

})();
</script>
"""

# Render the intro HTML once on first run so it overlays the app during load.
if not st.session_state.get('_st_intro_shown', False):
    try:
        components_html(_intro_html, height=160)
    except Exception:
        # Fallback to markdown if components fails
        st.markdown(_intro_html, unsafe_allow_html=True)
    st.session_state['_st_intro_shown'] = True
else:
    # Ensure the main app still receives the new styling when intro already shown
    try:
        # Extract CSS part to inject only the styles quickly
        css_part = _intro_html.split("<style>",1)[1].split("</style>",1)[0]
        components_html(f"<style>{css_part}</style>", height=1)
    except Exception:
        pass

# --- END: StyleTeller UI Enhancements ---


# --- ORIGINAL APP CODE (unchanged) ---

import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import json
import os
import time
import base64
import random

# --- INTRO & UI THEME INJECTION START ---
import time
try:
    import streamlit as st  # should already be imported but safe guard
    from streamlit.components.v1 import html as components_html
except Exception:
    pass

# Intro sequence: show a 4-second still image with fade in/out and background audio.
_intro_key = "_style_teller_intro_shown"
def show_intro_once():
    if st.session_state.get(_intro_key, False):
        return
    placeholder = st.empty()
    intro_html = """
    <div id="styleteller-intro" style="position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;
        background: rgba(255,255,255,0.0);backdrop-filter: blur(0px);">
      <div style="text-align:center;max-width:100%;width:100%;height:100%;display:flex;align-items:center;justify-content:center;">
        <div style="position:relative; display:flex; align-items:center; justify-content:center; width:100%; height:100%;">
          <img id="intro-img" src="https://i.ibb.co/B5qxJWW8/intro.png" style="max-width:70%; max-height:70%; opacity:0; transition: opacity 1.2s ease;" />
          <audio id="intro-audio" src="https://cdn.pixabay.com/download/audio/2021/08/04/audio_7e5b3f7c0c.mp3?filename=relaxing-piano-11248.mp3" preload="auto"></audio>
        </div>
      </div>
    </div>
    <script>
      (function() {
        const img = document.getElementById('intro-img');
        const audio = document.getElementById('intro-audio');
        // fade in image and audio
        setTimeout(()=>{ img.style.opacity = 1; try{ audio.volume=0.0; audio.play(); 
            // fade audio in
            let vol=0.0; const ramp = setInterval(()=>{ vol += 0.05; audio.volume = Math.min(vol,0.6); if(vol>=0.6) clearInterval(ramp); }, 100); }catch(e){} }, 50);
        // after 4s start fade out
        setTimeout(()=>{ img.style.opacity = 0; try{ 
            // fade audio out
            let vol = audio.volume; const ramp2 = setInterval(()=>{ vol -= 0.08; audio.volume = Math.max(vol,0); if(vol<=0){ audio.pause(); clearInterval(ramp2); } }, 80); }catch(e){} 
            // remove overlay from DOM after transition
            setTimeout(()=>{ const el = document.getElementById('styleteller-intro'); if(el) el.remove(); }, 1100);
        }, 4050);
      })();
    </script>
    """
    components_html(intro_html, height=600)
    # keep intro visible server-side for 4.2s to allow client animations to run
    time.sleep(4.2)
    placeholder.empty()
    st.session_state[_intro_key] = True

# run intro early (before main UI)
try:
    show_intro_once()
except Exception:
    pass

# Global CSS adjustments: background, page fade-in, logo, color boxes
global_css = """
<style>
/* Page fade-in */
html, body, .main, .block-container {
  animation: pageFadeIn 1s ease forwards;
  opacity: 0;
}
@keyframes pageFadeIn { from { opacity: 0; } to { opacity: 1; } }

/* Background image */
.stApp {
  background-image: url('https://i.ibb.co/gMDjN4Mt/background.jpg');
  background-size: cover !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
  position: relative;
}
/* white soft overlay */
.stApp::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.12);
  pointer-events: none;
  z-index: 0;
}

/* Force any black boxes to white with black text for contrast */
*[style*="background:#000"], *[style*="background:#000000"], *[style*="background: #000"], *[style*="background: #000000"] {
  background: #FFFFFF !important;
  color: #000000 !important;
}

/* Generic card overrides (Streamlit cards) */
.css-1d391kg, .css-18e3th9, .stButton, .stTextInput, .stSelectbox, .stTextArea {
  background: #FFFFFF !important;
  color: #000000 !important;
}

/* Logo placement at top center */
#styleteller-logo-wrap {
  text-align:center;
  width:100%;
  display:block;
  margin-top:10px;
  margin-bottom:8px;
  z-index: 2;
  position: relative;
}
#styleteller-logo-wrap img {
  max-height:88px;
  width:auto;
  opacity:0;
  transition: opacity 1s ease;
}
/* show logo after page fade */
html.loaded #styleteller-logo-wrap img { opacity: 1; }

/* Tiny tech dots decoration */
.tech-dot {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(0,150,255,0.95);
  box-shadow: 0 0 8px rgba(0,150,255,0.8);
  z-index: 1;
  opacity: 0.9;
}
</style>
<script>
// add 'loaded' class after content load to trigger logo appearance
window.addEventListener('load', function(){ document.documentElement.classList.add('loaded'); });

// randomly scatter some tech dots
function placeDots(count){
  for(let i=0;i<count;i++){
    const d = document.createElement('div');
    d.className='tech-dot';
    d.style.left = (Math.random()*90+2) + '%';
    d.style.top = (Math.random()*85+3) + '%';
    d.style.opacity = (0.4 + Math.random()*0.9);
    d.style.transform = 'scale(' + (0.6 + Math.random()*1.4) + ')';
    document.body.appendChild(d);
  }
}
setTimeout(()=>placeDots(28), 800);
</script>
"""

# Inject CSS/JS
try:
    st.markdown(global_css, unsafe_allow_html=True)
except Exception:
    try:
        components_html(global_css, height=0)
    except Exception:
        pass

# Insert top-center logo (will fade in with page)
try:
    st.markdown('<div class="logo-container"><img src="https://i.ibb.co/3YMDZQVn/logo.png" alt="Style Teller Logo"></div>', unsafe_allow_html=True)
except Exception:
    pass

# --- INTRO & UI THEME INJECTION END ---
# ---- Page Load & Logo Styling ----
# All fade-in CSS and logo placement code removed here
page_fadein_css = """
<style>
/* Keeping original global styles for consistency */
</style>
"""
st.markdown(page_fadein_css, unsafe_allow_html=True)

# ---- Display logo ----
# Removed logo display markdown to revert logo placement
# st.markdown(
#     """
#     <div class="logo-container">
#         <img src="logo.png" alt="Style Teller Logo" width="180">
#     </div>
#     """,
#     unsafe_allow_html=True
# )
# --- Logo Constant ---
# This Base64 string represents the logo image, allowing it to be embedded directly into the script.
LOGO_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4MoaAAAAAXNSR0IArs4c6QAAAXxJREFUeJzt2j9LA0EYB/BfE8GgCgqCKg4O4urNwc4WbGwQxM5OqS/gP0h+gvwT+C/g+B4qDpFw8Q1d+jO2wWd35uD0g/A8+B7cZ3nZ7u/2O1d8n2y7F+v9iP95t7xXn63j27/P57P5....." # Note: This is a placeholder for the full, extremely long Base64 string.

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
    st.markdown("""
        <style>
        /* Global Background Fix: Ensure app background is white */
        .stApp {
            background-color: #ffffff; /* White background */
        }
        
        /* 1. Ensure ALL text is BLACK for readability on white background */
        div, span, p, a, label, h1, h2, h3, h4, .stApp, 
        .st-emotion-cache-12fmw6v, 
        .st-emotion-cache-1fsy711 > div, 
        div[data-testid="stAppViewContainer"] * {
            color: #000000 !important;
        }
        
        /* --- EXCEPTION FOR DARK BACKGROUND UI ELEMENTS (Streamlit Sidebar/Top Menu) --- */
        /* This overrides the global black text for elements that remain on a dark background */
        div[data-testid="stSidebar"] *, /* All text in the dark sidebar */
        .st-emotion-cache-zq5aqc, /* Class for Streamlit's header/top-right menu container */
        .st-emotion-cache-9y213l, /* Class for 'Fork' link text */
        .st-emotion-cache-1g6h684, /* Class for the 3-dot menu icon/text */
        div[data-testid="stSidebarContent"] button, /* Button text inside the dark sidebar */
        .st-emotion-cache-5rimss /* Another common button text/icon class in sidebar */
        {
            color: #ffffff !important; /* Force text to white on dark background */
        }
        
        /* 1a. Ensure sidebar button backgrounds are transparent/dark so text is visible */
        div[data-testid="stSidebarContent"] button {
            background-color: transparent !important;
            border: 1px solid #ffffff33 !important; /* Light border for visibility */
        }
        /* End of sidebar/dark element exceptions */


        /* --- CRITICAL INPUT FIELD OVERRIDE (FIX for Black Boxes) --- */

        /* Target the actual input element for text, number, and password fields */
        div[data-baseweb="input"] input,
        div[data-baseweb="input"] textarea,
        div[data-baseweb="base-input"] input, 
        input[type="text"], 
        input[type="password"],
        input[type="number"],
        textarea {
            background-color: #ffffff !important; /* Force the field itself to white */
            color: #000000 !important; /* Force text to black */
            border: 1px solid #e0e0e0 !important; 
            -webkit-appearance: none; 
            appearance: none;
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

        /* --- BUTTON STYLING OVERRIDE (FIX for Black Buttons/Boxes) --- */

        /* Target all common button containers, including primary and secondary */
        /* .st-emotion-cache-1v0bb6x is the class for the PRIMARY button (The "Start Now" button) */
        /* Force Primary Button (Start Now) to white background / black text */
        div[data-testid="stVerticalBlock"] .st-emotion-cache-1v0bb6x, 
        .st-emotion-cache-1v0bb6x, /* Primary buttons (Start Now) */
        .st-emotion-cache-7ym5gk, /* Standard/Secondary buttons (Style buttons, Login/Signup) */
        div[data-testid*="stButton"] > button
        {
            background-color: #ffffff !important; /* White background */
            color: #000000 !important; /* Black text */
            border: 1px solid #000000 !important; /* Black border for distinction */
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
        
        /* Ensure button text remains black on hover/active states if needed */
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
        div[data-baseweb="popover"], /* The dropdown menu/popover container */
        div[role="listbox"], /* The list of options inside a selectbox */
        .st-emotion-cache-1fcpj1c, /* Generic Streamlit input wrapper */
        .st-emotion-cache-16j94j4 /* Another common input wrapper class */
        {
            background-color: #ffffff !important; 
            border: 1px solid #e0e0e0; /* Add a slight border for distinction */
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        /* --- END CRITICAL UI OVERRIDES --- */


        /* Sidebar Title Block fix for extra space (Req 5) */
        div[data-testid="stSidebarContent"] > div:nth-child(1) {
            padding-bottom: 0px !important; 
            margin-bottom: -10px !important;
        }


        /* --- Intro Video Fullscreen (Req 1) --- */
        /* Video fullscreen and visibility fixes removed */
        .video-active div[data-testid="stAppViewContainer"] {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 9999;
            background-color: #000000 !important; /* Black background for video mode */
            padding: 0 !important;
            margin: 0 !important;
        }
        
        /* Hide sidebar while video is active */
        .video-active div[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Center the video element */
        .video-active div[data-testid="stVerticalBlock"] {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        
        /* Make the video itself cover the screen */
        .video-active video {
             width: 100vw !important;
             height: 100vh !important;
             object-fit: cover !important; /* Ensure video covers the entire screen */
             margin: 0 !important;
             padding: 0 !important;
        }
        
        /* Hide the progress bar/text area when video is running, except for the progress bar itself */
        .video-active div[data-testid="stProgress"] * {
            color: white !important; /* Ensure progress text is visible on black background */
        }


        /* --- Standard Layout CSS retained below --- */

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
        
        </style>
        <script>
        // Use Javascript to toggle a class on the body to control video fullscreen
        function setVideoMode(isActive) {
            if (isActive) {
                document.body.classList.add('video-active');
            } else {
                document.body.classList.remove('video-active');
            }
        }
        </script>
    """, unsafe_allow_html=True)


# --- Page Functions ---

def intro_video():
    """Displays the intro video screen and automatically proceeds to login."""
    # Run JS to activate fullscreen mode CSS (Req 1)
    st.components.v1.html("<script>setVideoMode(true);</script>", height=0)
    
    # FIX: Replaced unreliable Google Drive link with a known, publicly hosted MP4 file
    VIDEO_URL = "https://static.videezy.com/system/resources/previews/000/054/104/original/10_Second_Countdown.mp4"
    st.video(VIDEO_URL, start_time=0)
    
    # Logic to auto-transition after a set time (simulates video completion)
    # Minimum 4 seconds watch time before auto-redirect (Req 1)
    MIN_DISPLAY_TIME = 4.0
    if "video_start_time" not in st.session_state:
        st.session_state["video_start_time"] = time.time()

    elapsed_time = time.time() - st.session_state["video_start_time"]
    
    if elapsed_time < MIN_DISPLAY_TIME:
        # Show progress bar and countdown text
        progress_text = f"Starting app... {int(MIN_DISPLAY_TIME - elapsed_time) + 1}s"
        st.progress(elapsed_time / MIN_DISPLAY_TIME, text=progress_text)
        time.sleep(1) 
        st.rerun() 
    else:
        # Auto-transition to login
        st.session_state["video_played"] = True
        st.session_state["page"] = "login"
        st.rerun()

def login_signup():
    """Login and Signup screen, now with Phone/OTP option (Req 3)."""
    # Run JS to deactivate fullscreen mode CSS
    st.components.v1.html("<script>setVideoMode(false);</script>", height=0)
    
    st.markdown("<h1 style='text-align: center;'>Style Teller</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='st-emotion-cache-6o6vcr'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Login or Sign Up</h2>", unsafe_allow_html=True)

    # Use a radio button/tabs for authentication method (Req 3)
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
        # Mock Phone/OTP Logic (Req 3)
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
    
    # Updated styles list (Req 4: Removed Boho, Vintage, Preppy, Gothic, Punk)
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
    # FIX for Requirement 5: Removed extra space using custom padding/margin in markdown.
    st.sidebar.markdown(
        "<div style='background-color: #f0f0f0; padding: 10px 0 0 0; border-radius: 10px;'>"
        "<h2 style='text-align: center; margin-bottom: 5px;'>Style Teller</h2>" 
        "<hr style='border: 1px solid #ccc; margin-top: 5px; margin-bottom: 10px;'>"
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
    
    # Updated styles list (Req 4: Removed Boho, Vintage, Preppy, Gothic, Punk)
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
        
    # NEW state variables for OTP logic (Req 3)
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


# --- MERGED STYLE TELLER UI UPDATE ---
import streamlit as st
from streamlit.components.v1 import html

# --- Page config ---
st.set_page_config(page_title="Style Teller", page_icon="👗", layout="wide")

# --- Inject custom CSS for centering logo and fixing layout ---
st.markdown("""
    <style>
    body {
        background-color: #0b0e11;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #0b0e11;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .logo-container img {
        height: 80px;
    }
    iframe, video {
        display: block;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logo Display (Top Center, visible on all screens) ---
st.markdown(
    '<div class="logo-container"><img src="logo.png" alt="Logo"></div>',
    unsafe_allow_html=True
)

# --- MAIN CONTENT ---
st.markdown("### Welcome to **Style Teller**")

try:
    # --- Example video section ---
    st.video("intro.mp4")

    # --- Example content or app logic ---
    st.markdown("""
        <div style='text-align:center; padding: 30px; color:white;'>
            <h2>Discover Your Style with AI</h2>
            <p>Upload your image and let Style Teller suggest fashion recommendations tailored to you.</p>
        </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred while loading content: {e}")

# --- Footer ---
st.markdown("""
    <div style='text-align:center; color: gray; margin-top: 50px;'>
        Created by sujal8454
    </div>
""", unsafe_allow_html=True)
