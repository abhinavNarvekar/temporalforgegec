# ==============================================================================
# FILE: app.py (Full Aesthetic Version)
# ==============================================================================

"""
Rhythm of the Machines - Main Entry Point
Home page with enhanced UI, sidebar, and floating icons
"""

import streamlit as st

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Rhythm of the Machines",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Initialize session state
# -------------------------------
for key in ["work_data", "mood_data", "rhythm_score", "analysis_complete"]:
    if key not in st.session_state:
        st.session_state[key] = None

# -------------------------------
# Custom Sidebar
# -------------------------------
st.markdown("""
<style>
/* Sidebar overall style */
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(160deg, #00D9FF 0%, #B794F6 50%, #FF6B9D 100%);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar headings */
.sidebar-heading {
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-align: center;
    color: #fff;
}

/* Sidebar buttons style */
.sidebar-button {
    display: block;
    width: 100%;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    border-radius: 15px;
    font-weight: 600;
    text-align: left;
    color: white !important;
    background: rgba(255,255,255,0.1);
    border: none;
    cursor: pointer;
    transition: 0.3s;
}

.sidebar-button:hover {
    background: rgba(255,255,255,0.3);
    transform: translateX(5px);
}
</style>

""", unsafe_allow_html=True)

# -------------------------------
# Hero Section with Floating Emojis
# -------------------------------
st.markdown("""
<div style='
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 6rem 2rem; 
    border-radius: 20px; 
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    text-align: center;
    color: white;
    position: relative;
'>
    <h1 style='font-size: 4rem; font-weight: 900;'>🤖 Rhythm of the Machines</h1>
    <h2 style='font-size: 2rem; font-weight: 400; margin-top: 1rem; color: #B794F6;'>
        Balance between Human & Machine Productivity
    </h2>
    <p style='margin-top: 1.5rem; font-size: 1.2rem; color: #d1d5db; line-height: 1.8;'>
        Harmonize your work metrics with wellbeing indicators. Our AI analyzes the delicate balance 
        between productivity and health, helping you find sustainable rhythm in the modern workplace.
    </p>
    <!-- Floating emojis -->
 
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------
# Feature Cards
# -------------------------------
feat_col1, feat_col2, feat_col3 = st.columns(3, gap="large")

cards = [
    ("🧠", "AI-Powered", "Smart Analysis", "#00D9FF", "rgba(0,217,255,0.1)"),
    ("📊", "Real-time Score", "Live Monitoring", "#B794F6", "rgba(183,148,246,0.1)"),
    ("💡", "Smart Insights", "Actionable Tips", "#FF6B9D", "rgba(255,107,157,0.1)")
]

for col, (icon, title, subtitle, color, bg) in zip([feat_col1, feat_col2, feat_col3], cards):
    col.markdown(f"""
        <div style='
            background: {bg};
            padding: 2rem 1rem;
            border-radius: 25px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        ' onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            <div style='font-size: 3rem;'>{icon}</div>
            <div style='font-weight: bold; font-size: 1.5rem; color: {color}; margin-top: 0.5rem;'>{title}</div>
            <div style='font-size: 1rem; color: #94a3b8; margin-top: 0.3rem;'>{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------------------
# Call-to-Action Button
# -------------------------------
st.markdown("""
<div style='text-align:center; margin-top:3rem;'>
    <a href="/Upload_Data" style='
        display:inline-block;
        padding: 1rem 3rem;
        font-size: 1.5rem;
        font-weight: 700;
        color:white;
        background: linear-gradient(135deg, #00D9FF, #B794F6, #FF6B9D);
        border-radius: 30px;
        text-decoration:none;
        box-shadow: 0 8px 30px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    ' onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
        🚀 Get Started
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# -------------------------------
# Footer Note
# -------------------------------
st.markdown("""
<div style='text-align:center; color:#94a3b8; font-size:0.9rem; margin-top:3rem;'>
    Designed with 💜 for productivity and wellbeing
</div>
""", unsafe_allow_html=True)
