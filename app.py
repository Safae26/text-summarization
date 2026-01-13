import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from transformers import pipeline
import requests
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="SummarizeAI | Soft Edition",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Asset Loading (Safe Mode) ---
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# Loading cute/friendly animations
lottie_robot = load_lottieurl("https://lottie.host/6b36056d-e461-4c12-9c3f-c3027602058e/s9Z3C4yX8h.json") # Cute bot
lottie_processing = load_lottieurl("https://lottie.host/933bb074-3253-487e-986b-a24140643b2f/S1q2s2yT4X.json") # Circles
lottie_coding = load_lottieurl("https://lottie.host/f8c0575d-3d44-482a-a922-383e536da808/U12s9Z3C4y.json") # Laptop

# --- Custom CSS (Animated Soft Theme) ---
st.markdown("""
<style>
    /* Import Cute Rounded Font */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&display=swap');

    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
        
    /* --- ANIMATIONS DEFINITIONS --- */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translate3d(0, 40px, 0); }
        to { opacity: 1; transform: translate3d(0, 0, 0); }
    }

    @keyframes pulse-soft {
        0% { box-shadow: 0 0 0 0 rgba(255, 154, 158, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(255, 154, 158, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 154, 158, 0); }
    }

    /* --- GLOBAL BACKGROUND --- */
    .stApp {
        background: linear-gradient(-45deg, #fdfbfb, #ebedee, #fdfbfb, #f3e7e9);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    /* --- TYPOGRAPHY --- */
    h1, h2, h3, h4, h5, p, label, li, .stMarkdown {
        font-family: 'Quicksand', sans-serif !important;
        color: #4A4E69;
    }
    
    p, li, label, .stMarkdown {
        color: #555 !important;
        font-size: 16px;
    }
    
    h1, h2, h3, h4, h5 {
        color: #4A4E69 !important; /* Deep Purple Grey */
        font-weight: 700;
        animation: fadeInUp 0.8s ease-out; /* Animate Headers */
    }

    /* --- GLASSMOPRHISM CARD (Animated) --- */
    .soft-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        padding: 25px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 1s both; /* Slide up animation */
    }
    
    .soft-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 15px 45px 0 rgba(31, 38, 135, 0.15);
    }

    /* --- INPUT AREAS --- */
    .stTextArea textarea {
        background-color: #ffffff !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 15px;
        padding: 15px;
        color: #333 !important;
        font-size: 15px;
        font-family: 'Quicksand', sans-serif !important;
        transition: border 0.3s;
    }
    .stTextArea textarea:focus {
        border-color: #ff9a9e !important; 
        box-shadow: 0 0 15px rgba(255, 154, 158, 0.2);
    }

    /* --- BUTTONS (Pulsing) --- */
    div.stButton > button {
        background: linear-gradient(to right, #ff9a9e 0%, #fecfef 99%, #fecfef 100%); 
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 12px 35px;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(255, 154, 158, 0.35);
        transition: all 0.3s ease;
        animation: pulse-soft 2s infinite; /* Heartbeat animation */
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(255, 154, 158, 0.6);
        color: #fff !important;
    }

    /* --- METRICS --- */
    div[data-testid="stMetricValue"] {
        font-family: 'Quicksand', sans-serif;
        color: #9A8C98;
        animation: fadeInUp 1.2s both;
    }

</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'animate' not in st.session_state:
    st.session_state.animate = False

# --- Model Loading ---
@st.cache_resource
def load_model():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# --- Main App ---
def main():
    
    # --- Sidebar ---
    with st.sidebar:
        st.markdown("<h2 style='text-align: center;'>🤖 SummarizeAI</h2>", unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Home", "Learn", "App"], 
            icons=['house-heart', 'journal-richtext', 'magic'],
            menu_icon="cast", 
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#9A8C98", "font-size": "18px"}, 
                "nav-link": {"font-family": "Quicksand", "font-size": "15px", "text-align": "left", "margin":"5px"},
                "nav-link-selected": {"background-color": "#fff", "color": "#ff9a9e", "box-shadow": "0 2px 10px rgba(0,0,0,0.05)"},
            }
        )
        st.markdown("---")
        st.caption("<b>Made with ❤️ by </b>", unsafe_allow_html=True)
        st.caption("Safae Eraji")
        st.caption("Naoual SOUIDI")
        st.caption("Isslam ZIANI")

    # --- HOME TAB ---
    if selected == "Home":
        st.title("Hi there, Reader! 👋")
        st.markdown("### Let's make reading easier.")
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.write("Welcome to your personal reading assistant. I can help you condense long articles, papers, or emails into sweet, short summaries.")
            
            # Applying the animated card class
            st.markdown("""
            <div class="soft-card">
                <h4>What can I do?</h4>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li><b>Summarize:</b> Paste any text up to 1000 words.</li>
                    <li><b>Save Time:</b> Get the gist in seconds ⏱️.</li>
                    <li><b>Understand:</b> I use advanced AI (BART) to rewrite text.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Try the App Now ➜"):
                st.info("Click 'App' in the sidebar!")

        with col2:
            if lottie_robot:
                st_lottie(lottie_robot, height=300, key="cute_robot")
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/2040/2040946.png", width=200)

    # --- LEARN TAB ---
    elif selected == "Learn":
        st.title("📚 How it Works")
        
        tab1, tab2 = st.tabs(["🧩 The Logic", "⚙️ The Brain"])
        
        with tab1:
            st.subheader("Extractive vs. Abstractive")
            st.write("Most simple tools just highlight sentences. I act more like a human:")
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("❌ **Old Way (Extractive)**")
                st.caption("Just copies sentences.")
                st.code("The cat sat. The cat ate.", language="text")
            with c2:
                st.markdown("✅ **Our Way (Abstractive)**")
                st.caption("Understands and rewrites.")
                st.code("The cat sat down to eat.", language="text")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab2:
            st.subheader("The Transformer Architecture")
            st.write("We use a model called **BART**. It has an Encoder (to read) and a Decoder (to write).")
            
    # --- APP TAB ---
    elif selected == "App":
        st.title("📝 Magic Summarizer")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("##### 1. Paste your text 👇")
            input_text = st.text_area("Input", height=200, placeholder="Paste your article or story here...", label_visibility="collapsed")
            
            with st.expander("⚙️ Tweak Settings (Optional)"):
                c1, c2 = st.columns(2)
                with c1:
                    min_L = st.slider("Min Length", 10, 50, 30)
                with c2:
                    max_L = st.slider("Max Length", 50, 300, 100)
            
            st.write("")
            # Button with new pulsing animation class via CSS
            if st.button("Summarize"):
                if not input_text:
                    st.warning("Please feed me some text first! 📄")
                else:
                    with col2:
                        status_box = st.empty()
                        with status_box:
                            if lottie_processing:
                                st_lottie(lottie_processing, height=120, key="loading")
                            else:
                                st.spinner("Thinking...")
                    
                    try:
                        summarizer = load_model()
                        
                        result = summarizer(input_text, max_length=max_L, min_length=min_L, do_sample=False)
                        st.session_state.summary = result[0]['summary_text']
                        # Trigger animation
                        st.session_state.animate = True
                        
                        # Clear loader
                        with col2:
                            status_box.empty()
                            
                    except Exception as e:
                        st.error(f"Oops! Something went wrong: {e}")

        # OUTPUT SECTION
        if st.session_state.summary:
            st.markdown("---")
            st.markdown("##### 2. Your Summary 🎉")
            
            # Container for the result
            result_container = st.empty()
            
            # ANIMATION LOGIC
            if st.session_state.animate:
                tokens = st.session_state.summary.split()
                current_text = ""
                # Animate word by word
                for token in tokens:
                    current_text += token + " "
                    # Re-render the HTML card with the new text and a sparkle cursor
                    result_container.markdown(f"""
                    <div class="soft-card" style="border-left: 5px solid #ff9a9e;">
                        <p style="font-size: 18px; line-height: 1.6; color: #444;">{current_text} ✨</p>
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.06) 
                
                # Turn off animation so it stays static on next rerun
                st.session_state.animate = False
                
                # Final render without the cursor
                result_container.markdown(f"""
                <div class="soft-card" style="border-left: 5px solid #ff9a9e;">
                    <p style="font-size: 18px; line-height: 1.6; color: #444;">{st.session_state.summary}</p>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                # Static render (if page reloads or sliders change)
                result_container.markdown(f"""
                <div class="soft-card" style="border-left: 5px solid #ff9a9e;">
                    <p style="font-size: 18px; line-height: 1.6; color: #444;">{st.session_state.summary}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Nice Metrics Display with Entrance Animation
            st.markdown('<div style="animation: fadeInUp 1s ease-out;">', unsafe_allow_html=True)
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Original Words", len(input_text.split()))
            with m2:
                st.metric("Summary Words", len(st.session_state.summary.split()))
            with m3:
                reduction = (1 - (len(st.session_state.summary.split())/len(input_text.split()))) * 100
                st.metric("Saved Reading", f"{reduction:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

"""
App Name: SummarizeAI | Soft Edition
Description: A Streamlit app that summarizes text using an abstractive model with a friendly UI.
Author: Safae Eraji, Naoual SOUIDI, Isslam ZIANI
License: MIT
Dependencies: streamlit, transformers, torch, beautifulsoup4, streamlit-lottie, streamlit-option-menu, requests
Date: 2025-01


Staying informed is essential yet time-consuming, with the
constant influx of diverse news stories. That is why SummarizeAI is here to providecontextually aware and human-like summaries!
It condenses lengthy articles into concise summaries, saving you time
while keeping you informed. Powered by advanced AI and NLP, it understands and
rewrites content, making it easier to grasp key points quickly.

All done using transformers, a class of neural networks. 
"""