# ==============================================================================
# FILE 1: app.py (Main Entry Point - Home Page)
# ==============================================================================

"""
Rhythm of the Machines - Main Entry Point
Home page and app configuration
"""

import streamlit as st
from utils.styling import apply_custom_css

# Page configuration
st.set_page_config(
    page_title="Rhythm of the Machines",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
apply_custom_css()

# Initialize session state
if 'work_data' not in st.session_state:
    st.session_state.work_data = None
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = None
if 'rhythm_score' not in st.session_state:
    st.session_state.rhythm_score = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# ==============================================================================
# HOME PAGE
# ==============================================================================

def home_page():
    """Landing page with animated introduction"""
    
    # Animated header with emojis
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <h1 style='font-size: 4rem; background: linear-gradient(135deg, #00D9FF 0%, #B794F6 50%, #FF6B9D 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;'>
                🤖❤️ Rhythm of the Machines
            </h1>
            <h2 style='color: #B794F6; font-size: 2rem; margin-bottom: 2rem;'>
                Balance between Human & Machine Productivity
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Description
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; font-size: 1.2rem; color: #94a3b8; line-height: 1.8;'>
                <p>Harmonize your work metrics with wellbeing indicators. Our AI analyzes the 
                delicate balance between productivity and health, helping you find sustainable 
                rhythm in the modern workplace.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Feature highlights
        feat1, feat2, feat3 = st.columns(3)
        with feat1:
            st.markdown("""
                <div style='text-align: center; padding: 1.5rem; background: rgba(0, 217, 255, 0.1); 
                            border-radius: 15px; margin: 1rem 0;'>
                    <div style='font-size: 3rem;'>🧠</div>
                    <div style='font-weight: bold; color: #00D9FF; margin-top: 0.5rem;'>AI-Powered</div>
                    <div style='color: #94a3b8; font-size: 0.9rem;'>Smart Analysis</div>
                </div>
            """, unsafe_allow_html=True)
        
        with feat2:
            st.markdown("""
                <div style='text-align: center; padding: 1.5rem; background: rgba(183, 148, 246, 0.1); 
                            border-radius: 15px; margin: 1rem 0;'>
                    <div style='font-size: 3rem;'>📊</div>
                    <div style='font-weight: bold; color: #B794F6; margin-top: 0.5rem;'>Real-time Score</div>
                    <div style='color: #94a3b8; font-size: 0.9rem;'>Live Monitoring</div>
                </div>
            """, unsafe_allow_html=True)
        
        with feat3:
            st.markdown("""
                <div style='text-align: center; padding: 1.5rem; background: rgba(255, 107, 157, 0.1); 
                            border-radius: 15px; margin: 1rem 0;'>
                    <div style='font-size: 3rem;'>💡</div>
                    <div style='font-weight: bold; color: #FF6B9D; margin-top: 0.5rem;'>Smart Insights</div>
                    <div style='color: #94a3b8; font-size: 0.9rem;'>Actionable Tips</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation message
        st.info("👈 Use the sidebar to navigate to **Upload Data** to get started!")
        
        # =============================
        # Get Started Button
        # =============================
        st.markdown("""
            <div style='text-align: center; margin-top: 3rem;'>
                <a href="/Upload_Data" style='
                    display: inline-block;
                    padding: 1rem 2rem;
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: white;
                    background: linear-gradient(135deg, #00D9FF 0%, #B794F6 50%, #FF6B9D 100%);
                    border-radius: 25px;
                    text-decoration: none;
                    transition: transform 0.2s ease;
                ' onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                    🚀 Get Started
                </a>
            </div>
        """, unsafe_allow_html=True)

# Run home page
home_page()
