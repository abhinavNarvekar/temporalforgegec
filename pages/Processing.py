# ==============================================================================
# FILE 6: pages/2_🧠_Processing.py
# ==============================================================================

"""
AI Processing Page
"""

import streamlit as st
import time
from utils.styling import apply_custom_css
from utils.analysis import calculate_rhythm_score

st.set_page_config(page_title="Processing", page_icon="🧠", layout="wide")
apply_custom_css()

# Check if data exists
if st.session_state.work_data is None or st.session_state.mood_data is None:
    st.error("No data found. Please upload data first.")
    if st.button("← Go to Upload Page"):
        st.switch_page("pages/1_📤_Upload_Data.py")
    st.stop()

st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='background: linear-gradient(135deg, #00D9FF 0%, #FF6B9D 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🧠 Analyzing Your Rhythm
        </h1>
        <p style='font-size: 1.2rem; color: #94a3b8;'>
            AI is processing your data patterns...
        </p>
    </div>
""", unsafe_allow_html=True)

# Center the progress animation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style='text-align: center; font-size: 5rem; margin: 2rem 0;'>
            🤖❤️
        </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Processing steps
    steps = [
        ("Parsing CSV data and validating formats", 20),
        ("Detecting productivity patterns and work cycles", 40),
        ("Correlating wellbeing with work intensity", 60),
        ("Calculating Rhythm Score and anomalies", 80),
        ("Generating personalized insights", 100)
    ]
    
    for step_text, progress in steps:
        status_text.markdown(f"""
            <div style='text-align: center; color: #B794F6; font-size: 1.1rem; margin: 1rem 0;'>
                {step_text}...
            </div>
        """, unsafe_allow_html=True)
        progress_bar.progress(progress)
        time.sleep(0.8)
    
    # Perform actual analysis
    if not st.session_state.analysis_complete:
        with st.spinner('Finalizing analysis...'):
            analysis_results = calculate_rhythm_score(
                st.session_state.work_data,
                st.session_state.mood_data
            )
            st.session_state.rhythm_score = analysis_results
            st.session_state.analysis_complete = True
    
    st.success("✅ Analysis Complete!")
    time.sleep(1)
    
    # Navigate to dashboard
    st.switch_page("pages/Dashboard.py")

