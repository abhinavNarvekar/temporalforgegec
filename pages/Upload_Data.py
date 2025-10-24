# ==============================================================================
# FILE 5: pages/1_📤_Upload_Data.py
# ==============================================================================

"""
Data Upload Page - Modern Rectangular Header Version
"""

import streamlit as st
import pandas as pd
from utils.styling import apply_custom_css
from utils.analysis import validate_csv_format, generate_sample_data

# =========================
# ✅ Initialize session variables safely
# =========================
for key in ["work_data", "mood_data", "analysis_complete"]:
    if key not in st.session_state:
        st.session_state[key] = None

# =========================
# Page config & custom CSS
# =========================
st.set_page_config(page_title="Upload Data", page_icon="📤", layout="wide")
apply_custom_css()

# =========================
# Page header as a modern rectangular card
# =========================
st.markdown("""
<div style='
    max-width: 700px;
    margin: 2rem auto;
    padding: 2rem 2.5rem;
    border-radius: 25px;
    background: linear-gradient(135deg, #00D9FF, #B794F6, #FF6B9D);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    text-align: center;
    color: white;
'>
    <h1 style='font-size: 3rem; font-weight: 900; margin: 0;'>📤 Upload Your Data</h1>
    <p style='font-size: 1.2rem; margin-top: 0.5rem; color: #f0f0f0; line-height: 1.5;'>
        Feed the rhythm with your productivity and wellbeing metrics
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# Upload columns
# =========================
col1, col2 = st.columns(2, gap="large")

# =========================
# Machine Productivity Upload
# =========================
with col1:
    st.markdown("""
        <div style='padding: 1.5rem; background: rgba(0, 217, 255, 0.05); 
                    border: 2px solid #00D9FF; border-radius: 20px; margin-bottom: 2rem;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1); transition: transform 0.2s ease;'>
            <h3 style='color: #00D9FF;'>🤖 Machine Productivity</h3>
        </div>
    """, unsafe_allow_html=True)
    
    work_file = st.file_uploader(
        "Upload work data CSV",
        type=['csv'],
        key='work_upload',
        help="Upload your work hours, tasks completed, and productivity metrics"
    )
    
    with st.expander("📋 See Expected Format"):
        st.code("""
date,work_hours,tasks_completed,server_uptime
2025-01-01,8.5,12,99.8
2025-01-02,7.0,10,99.9
2025-01-03,9.5,15,99.7
        """, language='csv')
        st.info("**Required columns:** date, work_hours, tasks_completed")
    
    if work_file:
        try:
            work_df = pd.read_csv(work_file)
            work_df['date'] = pd.to_datetime(work_df['date'])
            
            is_valid, message = validate_csv_format(work_df, 'work')
            if is_valid:
                st.session_state.work_data = work_df
                st.success(f"✅ Loaded {len(work_df)} days of work data")
                st.dataframe(work_df.head(), use_container_width=True)
            else:
                st.error(f"❌ {message}")
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# =========================
# Human Wellbeing Upload
# =========================
with col2:
    st.markdown("""
        <div style='padding: 1.5rem; background: rgba(255, 107, 157, 0.05); 
                    border: 2px solid #FF6B9D; border-radius: 20px; margin-bottom: 2rem;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1); transition: transform 0.2s ease;'>
            <h3 style='color: #FF6B9D;'>❤️ Human Wellbeing</h3>
        </div>
    """, unsafe_allow_html=True)
    
    mood_file = st.file_uploader(
        "Upload wellbeing data CSV",
        type=['csv'],
        key='mood_upload',
        help="Upload your mood scores, stress levels, and sleep data"
    )
    
    with st.expander("📋 See Expected Format"):
        st.code("""
date,mood_score,stress_level,sleep_hours
2025-01-01,7,4,7.5
2025-01-02,8,3,8.0
2025-01-03,6,6,6.5
        """, language='csv')
        st.info("**Required columns:** date, mood_score, stress_level, sleep_hours")
    
    if mood_file:
        try:
            mood_df = pd.read_csv(mood_file)
            mood_df['date'] = pd.to_datetime(mood_df['date'])
            
            is_valid, message = validate_csv_format(mood_df, 'mood')
            if is_valid:
                st.session_state.mood_data = mood_df
                st.success(f"✅ Loaded {len(mood_df)} days of wellbeing data")
                st.dataframe(mood_df.head(), use_container_width=True)
            else:
                st.error(f"❌ {message}")
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

# =========================
# Analyze button
# =========================
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.work_data is not None and st.session_state.mood_data is not None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Analyze Rhythm", key="analyze"):
            st.session_state.analysis_complete = False
            st.switch_page("pages/Processing.py")
else:
    st.warning("⚠️ Please upload both CSV files to proceed with analysis")

# =========================
# Sample data option
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🎲 Don't have data? Use sample dataset"):
    if st.button("Load Sample Data"):
        work_data, mood_data = generate_sample_data()
        st.session_state.work_data = work_data
        st.session_state.mood_data = mood_data
        st.success("✅ Sample data loaded! Click 'Analyze Rhythm' to continue.")
        st.rerun()
