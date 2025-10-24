"""
Rhythm of the Machines - Streamlit Application
A hackathon project that monitors the balance between machine productivity and human wellbeing
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Rhythm of the Machines",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CUSTOM CSS STYLING
# ==============================================================================
st.markdown("""
<style>
    /* Main color palette */
    :root {
        --machine-color: #00D9FF;
        --human-color: #FF6B9D;
        --balance-color: #B794F6;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #00D9FF 0%, #FF6B9D 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 15px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(0, 217, 255, 0.3);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        border: 2px dashed #00D9FF;
        border-radius: 15px;
        padding: 2rem;
        background-color: rgba(0, 217, 255, 0.05);
    }
    
    /* Alert boxes */
    .alert-success {
        background-color: rgba(74, 222, 128, 0.1);
        border-left: 4px solid #4ADE80;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: rgba(251, 191, 36, 0.1);
        border-left: 4px solid #FBBF24;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .alert-danger {
        background-color: rgba(248, 113, 113, 0.1);
        border-left: 4px solid #F87171;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'work_data' not in st.session_state:
    st.session_state.work_data = None
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = None
if 'rhythm_score' not in st.session_state:
    st.session_state.rhythm_score = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# ==============================================================================
# HELPER FUNCTIONS FOR AI ANALYSIS
# ==============================================================================

def validate_csv_format(df, data_type):
    """Validate CSV format based on data type (work or mood)"""
    required_columns = {
        'work': ['date', 'work_hours', 'tasks_completed'],
        'mood': ['date', 'mood_score', 'stress_level', 'sleep_hours']
    }
    
    if data_type not in required_columns:
        return False, "Invalid data type"
    
    missing_cols = set(required_columns[data_type]) - set(df.columns)
    if missing_cols:
        return False, f"Missing columns: {', '.join(missing_cols)}"
    
    return True, "Valid format"

def calculate_rhythm_score(work_df, mood_df):
    """
    AI-powered calculation of Rhythm Score
    Placeholder for actual ML model implementation
    """
    # Merge datasets on date
    merged_df = pd.merge(work_df, mood_df, on='date', how='inner')
    
    # Calculate component scores (0-100 scale)
    # Machine productivity score
    avg_work_hours = merged_df['work_hours'].mean()
    avg_tasks = merged_df['tasks_completed'].mean()
    machine_score = min(100, (avg_work_hours / 8 * 50 + avg_tasks / 10 * 50))
    
    # Human wellbeing score
    avg_mood = merged_df['mood_score'].mean()
    avg_stress = merged_df['stress_level'].mean()
    avg_sleep = merged_df['sleep_hours'].mean()
    human_score = (avg_mood / 10 * 40 + (10 - avg_stress) / 10 * 30 + avg_sleep / 8 * 30)
    
    # Balance penalty - penalize extreme imbalances
    imbalance = abs(machine_score - human_score)
    balance_penalty = (imbalance / 100) * 20
    
    # Final rhythm score
    rhythm_score = (machine_score + human_score) / 2 - balance_penalty
    
    return {
        'rhythm_score': round(rhythm_score, 1),
        'machine_score': round(machine_score, 1),
        'human_score': round(human_score, 1),
        'avg_work_hours': round(avg_work_hours, 1),
        'avg_mood': round(avg_mood, 1),
        'avg_stress': round(avg_stress, 1),
        'avg_sleep': round(avg_sleep, 1),
        'correlation': round(merged_df['work_hours'].corr(merged_df['mood_score']), 2),
        'merged_data': merged_df
    }

def detect_anomalies(merged_df):
    """
    AI-powered anomaly detection
    Placeholder for actual ML anomaly detection
    """
    anomalies = []
    
    # Detect burnout risk (high work + low mood)
    burnout_days = merged_df[
        (merged_df['work_hours'] > 10) & (merged_df['mood_score'] < 5)
    ]
    if len(burnout_days) > 0:
        anomalies.append({
            'type': 'danger',
            'title': 'Burnout Risk Detected',
            'description': f'{len(burnout_days)} days with 10+ work hours and mood below 5',
            'icon': '🚨'
        })
    
    # Detect sleep deficit
    sleep_deficit = merged_df[merged_df['sleep_hours'] < 6]
    if len(sleep_deficit) > 3:
        anomalies.append({
            'type': 'warning',
            'title': 'Sleep Deficit Pattern',
            'description': f'{len(sleep_deficit)} days with less than 6 hours of sleep',
            'icon': '😴'
        })
    
    # Detect positive trends
    if len(merged_df) > 7:
        recent_mood = merged_df.tail(7)['mood_score'].mean()
        earlier_mood = merged_df.head(7)['mood_score'].mean()
        if recent_mood > earlier_mood + 1:
            anomalies.append({
                'type': 'success',
                'title': 'Positive Mood Trend',
                'description': f'Mood improved by {round(recent_mood - earlier_mood, 1)} points in recent week',
                'icon': '✨'
            })
    
    # Detect overwork periods
    consecutive_overwork = 0
    max_consecutive = 0
    for hours in merged_df['work_hours']:
        if hours > 9:
            consecutive_overwork += 1
            max_consecutive = max(max_consecutive, consecutive_overwork)
        else:
            consecutive_overwork = 0
    
    if max_consecutive >= 3:
        anomalies.append({
            'type': 'warning',
            'title': 'Extended Overwork Period',
            'description': f'{max_consecutive} consecutive days with 9+ work hours',
            'icon': '⚠️'
        })
    
    return anomalies

def generate_insights(analysis_results):
    """
    AI-generated personalized insights
    Placeholder for actual NLP/LLM integration
    """
    insights = []
    
    merged_df = analysis_results['merged_data']
    correlation = analysis_results['correlation']
    
    # Insight 1: Peak productivity pattern
    merged_df['hour_category'] = pd.cut(merged_df['work_hours'], 
                                         bins=[0, 7, 9, 24], 
                                         labels=['Low', 'Optimal', 'High'])
    mood_by_hours = merged_df.groupby('hour_category')['mood_score'].mean()
    
    best_category = mood_by_hours.idxmax()
    insights.append({
        'icon': '📈',
        'title': 'Peak Productivity Pattern',
        'description': f'Your mood is highest during {best_category} work hour days (avg mood: {mood_by_hours.max():.1f})',
        'recommendation': 'Structure your week to maintain optimal work duration. Quality over quantity leads to better outcomes.',
        'color': 'machine'
    })
    
    # Insight 2: Work-wellbeing correlation
    if correlation < -0.3:
        insights.append({
            'icon': '💔',
            'title': 'Negative Work-Wellbeing Link',
            'description': f'Strong negative correlation detected ({correlation}). More work hours consistently lower your mood.',
            'recommendation': 'Implement strict work boundaries. Consider delegating tasks or requesting workload adjustment.',
            'color': 'human'
        })
    elif correlation > 0.3:
        insights.append({
            'icon': '💚',
            'title': 'Positive Work-Wellbeing Link',
            'description': f'Positive correlation detected ({correlation}). Your work energizes you when properly balanced.',
            'recommendation': 'You thrive on productivity! Maintain current balance and protect against future overwork.',
            'color': 'balance'
        })
    
    # Insight 3: Sleep impact
    sleep_mood_corr = merged_df['sleep_hours'].corr(merged_df['mood_score'])
    if sleep_mood_corr > 0.4:
        insights.append({
            'icon': '😴',
            'title': 'Sleep is Your Superpower',
            'description': f'Strong link between sleep and mood (correlation: {sleep_mood_corr:.2f})',
            'recommendation': f'Prioritize {merged_df["sleep_hours"].quantile(0.75):.1f}+ hours of sleep. Your data shows this directly improves your wellbeing.',
            'color': 'human'
        })
    
    # Insight 4: Optimal work range
    optimal_work = merged_df[merged_df['mood_score'] >= 7]['work_hours'].median()
    insights.append({
        'icon': '🎯',
        'title': 'Your Sweet Spot Identified',
        'description': f'You maintain high mood (7+) with around {optimal_work:.1f} work hours per day',
        'recommendation': f'Target {optimal_work:.1f} hours as your baseline. Current adherence: {len(merged_df[abs(merged_df["work_hours"] - optimal_work) < 1]) / len(merged_df) * 100:.0f}% of days.',
        'color': 'balance'
    })
    
    return insights

# ==============================================================================
# PAGE 1: HOME PAGE
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
    
    # Animated description with rotating emojis
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
        
        # Feature highlights in columns
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
        
        # Get Started button
        if st.button("🚀 Get Started", key="get_started"):
            st.session_state.page = 'upload'
            st.rerun()

# ==============================================================================
# PAGE 2: DATA UPLOAD PAGE
# ==============================================================================

def upload_page():
    """Data upload page with clear instructions"""
    
    st.markdown("""
        <h1 style='background: linear-gradient(135deg, #00D9FF 0%, #FF6B9D 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            📤 Upload Your Data
        </h1>
        <p style='font-size: 1.2rem; color: #94a3b8; margin-bottom: 2rem;'>
            Feed the rhythm with your productivity and wellbeing metrics
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Machine Productivity Upload
    with col1:
        st.markdown("""
            <div style='padding: 1.5rem; background: rgba(0, 217, 255, 0.05); 
                        border: 2px solid #00D9FF; border-radius: 20px; margin-bottom: 2rem;'>
                <h3 style='color: #00D9FF;'>🤖 Machine Productivity</h3>
            </div>
        """, unsafe_allow_html=True)
        
        work_file = st.file_uploader(
            "Upload work data CSV",
            type=['csv'],
            key='work_upload',
            help="Upload your work hours, tasks completed, and productivity metrics"
        )
        
        # Show example format
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
    
    # Human Wellbeing Upload
    with col2:
        st.markdown("""
            <div style='padding: 1.5rem; background: rgba(255, 107, 157, 0.05); 
                        border: 2px solid #FF6B9D; border-radius: 20px; margin-bottom: 2rem;'>
                <h3 style='color: #FF6B9D;'>❤️ Human Wellbeing</h3>
            </div>
        """, unsafe_allow_html=True)
        
        mood_file = st.file_uploader(
            "Upload wellbeing data CSV",
            type=['csv'],
            key='mood_upload',
            help="Upload your mood scores, stress levels, and sleep data"
        )
        
        # Show example format
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
    
    # Analyze button (only enabled when both files uploaded)
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.work_data is not None and st.session_state.mood_data is not None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔍 Analyze Rhythm", key="analyze"):
                st.session_state.page = 'processing'
                st.session_state.analysis_complete = False
                st.rerun()
    else:
        st.warning("⚠️ Please upload both CSV files to proceed with analysis")
    
    # Sample data option
    st.markdown("<br><br>", unsafe_allow_html=True)
    with st.expander("🎲 Don't have data? Use sample dataset"):
        if st.button("Load Sample Data"):
            # Generate sample data
            dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
            
            # Sample work data
            work_data = pd.DataFrame({
                'date': dates,
                'work_hours': np.random.normal(8, 1.5, 30).clip(5, 12),
                'tasks_completed': np.random.poisson(10, 30),
                'server_uptime': np.random.uniform(98, 100, 30)
            })
            
            # Sample mood data (inversely correlated with work hours)
            mood_data = pd.DataFrame({
                'date': dates,
                'mood_score': (10 - work_data['work_hours'] * 0.5 + np.random.normal(0, 1, 30)).clip(1, 10),
                'stress_level': (work_data['work_hours'] * 0.5 + np.random.normal(0, 1, 30)).clip(1, 10),
                'sleep_hours': (9 - work_data['work_hours'] * 0.2 + np.random.normal(0, 0.5, 30)).clip(5, 9)
            })
            
            st.session_state.work_data = work_data
            st.session_state.mood_data = mood_data
            st.success("✅ Sample data loaded! Click 'Analyze Rhythm' to continue.")
            st.rerun()

# ==============================================================================
# PAGE 3: AI PROCESSING PAGE
# ==============================================================================

def processing_page():
    """AI processing animation and analysis"""
    
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
        # Animated icon
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
            time.sleep(0.8)  # Simulate processing time
        
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
        st.session_state.page = 'dashboard'
        st.rerun()

# ==============================================================================
# PAGE 4: DASHBOARD / RESULTS PAGE
# ==============================================================================

def dashboard_page():
    """Main dashboard with rhythm score and visualizations"""
    
    if st.session_state.rhythm_score is None:
        st.error("No analysis results found. Please upload data first.")
        if st.button("← Back to Upload"):
            st.session_state.page = 'upload'
            st.rerun()
        return
    
    results = st.session_state.rhythm_score
    merged_df = results['merged_data']
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
            <h1 style='background: linear-gradient(135deg, #00D9FF 0%, #FF6B9D 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                📊 Your Rhythm Dashboard
            </h1>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='color: #94a3b8; font-size: 1.1rem;'>Analysis Period: {merged_df['date'].min().strftime('%b %d')} - {merged_df['date'].max().strftime('%b %d, %Y')}</p>", unsafe_allow_html=True)
    
    with col2:
        if st.button("📥 Export Report"):
            st.info("Report export functionality - placeholder for CSV/PDF download")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Central Rhythm Score
    st.markdown("""
        <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(255, 107, 157, 0.1) 100%); 
                    border-radius: 30px; margin-bottom: 2rem; box-shadow: 0 10px 40px rgba(183, 148, 246, 0.2);'>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Create circular gauge visualization
        rhythm_score = results['rhythm_score']
        
        # Determine status and color
        if rhythm_score >= 75:
            status = "Excellent"
            color = "#4ADE80"
        elif rhythm_score >= 60:
            status = "Balanced"
            color = "#B794F6"
        elif rhythm_score >= 45:
            status = "Moderate"
            color = "#FBBF24"
        else:
            status = "Needs Attention"
            color = "#F87171"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=rhythm_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Rhythm Score", 'font': {'size': 24, 'color': '#B794F6'}},
            number={'font': {'size': 60, 'color': color}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "gray"},
                'bar': {'color': color},
                'bgcolor': "rgba(255,255,255,0.1)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 45], 'color': 'rgba(248, 113, 113, 0.2)'},
                    {'range': [45, 60], 'color': 'rgba(251, 191, 36, 0.2)'},
                    {'range': [60, 75], 'color': 'rgba(183, 148, 246, 0.2)'},
                    {'range': [75, 100], 'color': 'rgba(74, 222, 128, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white", 'family': "Arial"},
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
            <div style='text-align: center; font-size: 1.5rem; color: {color}; font-weight: bold; margin-top: -2rem;'>
                {status}
            </div>
        """, unsafe_allow_html=True)
        
        # Component scores
        st.markdown(f"""
            <div style='display: flex; justify-content: center; gap: 3rem; margin-top: 2rem;'>
                <div style='text-align: center;'>
                    <div style='color: #00D9FF; font-size: 2rem; font-weight: bold;'>🤖 {results['machine_score']}</div>
                    <div style='color: #94a3b8;'>Machine Score</div>
                </div>
                <div style='text-align: center;'>
                    <div style='color: #FF6B9D; font-size: 2rem; font-weight: bold;'>❤️ {results['human_score']}</div>
                    <div style='color: #94a3b8;'>Human Score</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Stats Cards
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Avg Work Hours",
            value=f"{results['avg_work_hours']}h",
            delta=f"+5%" if results['avg_work_hours'] > 8 else "-3%"
        )
    
    with col2:
        st.metric(
            label="😊 Avg Mood Score",
            value=f"{results['avg_mood']}/10",
            delta=f"{'+' if results['avg_mood'] > 7 else ''}{round((results['avg_mood'] - 7) * 10)}%"
        )
    
    with col3:
        st.metric(
            label="😴 Avg Sleep",
            value=f"{results['avg_sleep']}h",
            delta=f"+{round((results['avg_sleep'] - 7) * 100 / 7)}%" if results['avg_sleep'] > 7 else f"{round((results['avg_sleep'] - 7) * 100 / 7)}%"
        )
    
    with col4:
        corr_status = "Strong" if abs(results['correlation']) > 0.5 else "Moderate" if abs(results['correlation']) > 0.3 else "Weak"
        st.metric(
            label="🔗 Correlation",
            value=results['correlation'],
            delta=corr_status
        )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Main Chart and Alerts Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Productivity vs Wellbeing Trends")
        
        # Create dual-axis chart
        fig = go.Figure()
        
        # Add work hours trace
        fig.add_trace(go.Scatter(
            x=merged_df['date'],
            y=merged_df['work_hours'],
            name='Work Hours',
            line=dict(color='#00D9FF', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 217, 255, 0.1)'
        ))
        
        # Add mood score trace (scaled to match work hours range)
        mood_scaled = merged_df['mood_score'] * (merged_df['work_hours'].max() / 10)
        fig.add_trace(go.Scatter(
            x=merged_df['date'],
            y=mood_scaled,
            name='Mood Score',
            line=dict(color='#FF6B9D', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 157, 0.1)',
            yaxis='y2'
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(21, 27, 59, 0.5)",
            font={'color': "white"},
            xaxis=dict(title="Date", gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title="Work Hours", gridcolor='rgba(255,255,255,0.1)', range=[0, merged_df['work_hours'].max() + 2]),
            yaxis2=dict(
                title="Mood Score",
                overlaying='y',
                side='right',
                gridcolor='rgba(255,255,255,0.05)',
                range=[0, 10 * (merged_df['work_hours'].max() / 10) + 2]
            ),
            hovermode='x unified',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Insight box below chart
        st.markdown(f"""
            <div class='alert-{('success' if results['correlation'] > 0 else 'warning')}'>
                <strong>🧠 AI Insight:</strong> {
                    f"Strong negative correlation detected. When work hours increase, mood tends to decrease by {abs(results['correlation']) * 100:.0f}%." 
                    if results['correlation'] < -0.3 
                    else f"Positive correlation found. Your work energizes you when balanced properly." 
                    if results['correlation'] > 0.3 
                    else "Weak correlation between work hours and mood. Other factors may be more influential."
                }
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚨 Active Alerts")
        
        # Detect and display anomalies
        anomalies = detect_anomalies(merged_df)
        
        if not anomalies:
            st.markdown("""
                <div class='alert-success'>
                    <strong>✅ All Clear!</strong><br>
                    No major imbalances detected. Keep up the good work!
                </div>
            """, unsafe_allow_html=True)
        else:
            for anomaly in anomalies:
                alert_class = f"alert-{anomaly['type']}"
                st.markdown(f"""
                    <div class='{alert_class}'>
                        <strong>{anomaly['icon']} {anomaly['title']}</strong><br>
                        <small>{anomaly['description']}</small>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Navigation to insights
        if st.button("💡 View Detailed Insights", key="view_insights"):
            st.session_state.page = 'insights'
            st.rerun()
    
    # Additional visualizations
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 Work Intensity Heatmap")
        
        # Create a weekly heatmap
        merged_df['day_of_week'] = merged_df['date'].dt.day_name()
        merged_df['week'] = merged_df['date'].dt.isocalendar().week
        
        pivot_data = merged_df.pivot_table(
            values='work_hours',
            index='day_of_week',
            columns='week',
            aggfunc='mean'
        )
        
        # Reorder days of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_data = pivot_data.reindex([day for day in day_order if day in pivot_data.index])
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=[f"Week {int(w)}" for w in pivot_data.columns],
            y=pivot_data.index,
            colorscale=[[0, '#1a1f4d'], [0.5, '#B794F6'], [1, '#00D9FF']],
            text=pivot_data.values.round(1),
            texttemplate='%{text}h',
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "white"},
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 😊 Mood Distribution")
        
        # Create mood distribution chart
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=merged_df['mood_score'],
            name='Mood Score',
            marker_color='#FF6B9D',
            boxmean='sd'
        ))
        
        fig.add_trace(go.Box(
            y=10 - merged_df['stress_level'],
            name='Low Stress (inverted)',
            marker_color='#B794F6',
            boxmean='sd'
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(21, 27, 59, 0.5)",
            font={'color': "white"},
            yaxis=dict(title="Score (1-10)", gridcolor='rgba(255,255,255,0.1)', range=[0, 11]),
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# PAGE 5: INSIGHTS / RECOMMENDATIONS PAGE
# ==============================================================================

def insights_page():
    """AI-generated insights and recommendations"""
    
    if st.session_state.rhythm_score is None:
        st.error("No analysis results found. Please upload data first.")
        if st.button("← Back to Upload"):
            st.session_state.page = 'upload'
            st.rerun()
        return
    
    results = st.session_state.rhythm_score
    
    # Header
    st.markdown("""
        <h1 style='background: linear-gradient(135deg, #00D9FF 0%, #FF6B9D 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            💡 AI-Generated Insights
        </h1>
        <p style='font-size: 1.2rem; color: #94a3b8; margin-bottom: 3rem;'>
            Personalized recommendations based on your rhythm analysis
        </p>
    """, unsafe_allow_html=True)
    
    # Generate insights
    insights = generate_insights(results)
    
    # Display insights in a grid
    cols = st.columns(2)
    for idx, insight in enumerate(insights):
        with cols[idx % 2]:
            # Determine background color based on insight type
            bg_colors = {
                'machine': 'rgba(0, 217, 255, 0.05)',
                'human': 'rgba(255, 107, 157, 0.05)',
                'balance': 'rgba(183, 148, 246, 0.05)'
            }
            border_colors = {
                'machine': '#00D9FF',
                'human': '#FF6B9D',
                'balance': '#B794F6'
            }
            
            bg_color = bg_colors.get(insight['color'], bg_colors['balance'])
            border_color = border_colors.get(insight['color'], border_colors['balance'])
            
            st.markdown(f"""
                <div style='padding: 2rem; background: {bg_color}; 
                            border-left: 4px solid {border_color}; border-radius: 15px; 
                            margin-bottom: 1.5rem; min-height: 250px;'>
                    <div style='font-size: 2.5rem; margin-bottom: 1rem;'>{insight['icon']}</div>
                    <h3 style='color: white; margin-bottom: 1rem;'>{insight['title']}</h3>
                    <p style='color: #94a3b8; margin-bottom: 1rem;'>{insight['description']}</p>
                    <div style='background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 10px;'>
                        <strong style='color: {border_color};'>💡 Recommendation:</strong><br>
                        <span style='color: #cbd5e1; font-size: 0.95rem;'>{insight['recommendation']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Historical Trends Section
    st.markdown("### 📊 Historical Rhythm Trends")
    
    merged_df = results['merged_data']
    
    # Calculate weekly rhythm scores
    merged_df['week'] = merged_df['date'].dt.isocalendar().week
    weekly_scores = []
    
    for week in merged_df['week'].unique():
        week_data = merged_df[merged_df['week'] == week]
        week_machine = (week_data['work_hours'].mean() / 8 * 50 + week_data['tasks_completed'].mean() / 10 * 50)
        week_human = (week_data['mood_score'].mean() / 10 * 40 + 
                     (10 - week_data['stress_level'].mean()) / 10 * 30 + 
                     week_data['sleep_hours'].mean() / 8 * 30)
        week_rhythm = (week_machine + week_human) / 2
        weekly_scores.append({
            'week': f"Week {int(week)}",
            'score': round(week_rhythm, 1),
            'machine': round(week_machine, 1),
            'human': round(week_human, 1)
        })
    
    # Create trend visualization
    weekly_df = pd.DataFrame(weekly_scores)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=weekly_df['week'],
        y=weekly_df['score'],
        name='Rhythm Score',
        marker=dict(
            color=weekly_df['score'],
            colorscale=[[0, '#F87171'], [0.5, '#FBBF24'], [0.7, '#B794F6'], [1, '#4ADE80']],
            showscale=False
        ),
        text=weekly_df['score'],
        textposition='outside',
        textfont=dict(size=14, color='white')
    ))
    
    # Add trend line
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['score'],
        mode='lines+markers',
        name='Trend',
        line=dict(color='#B794F6', width=3, dash='dash'),
        marker=dict(size=10, color='#B794F6')
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(21, 27, 59, 0.5)",
        font={'color': "white"},
        yaxis=dict(title="Rhythm Score", gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
        xaxis=dict(title="Time Period", gridcolor='rgba(255,255,255,0.1)'),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Trend analysis
    if len(weekly_scores) >= 2:
        trend = weekly_scores[-1]['score'] - weekly_scores[0]['score']
        trend_emoji = "📈" if trend > 5 else "📉" if trend < -5 else "➡️"
        trend_text = "improving" if trend > 5 else "declining" if trend < -5 else "stable"
        trend_color = "#4ADE80" if trend > 5 else "#F87171" if trend < -5 else "#FBBF24"
        
        st.markdown(f"""
            <div style='text-align: center; padding: 2rem; background: rgba(183, 148, 246, 0.1); 
                        border-radius: 15px; margin-top: 2rem;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>{trend_emoji}</div>
                <p style='font-size: 1.3rem; color: {trend_color}; font-weight: bold;'>
                    Your rhythm is {trend_text}
                </p>
                <p style='color: #94a3b8;'>
                    {abs(trend):.1f} point {'increase' if trend > 0 else 'decrease'} from week 1 to week {len(weekly_scores)}
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Full Report", use_container_width=True):
            # Create a comprehensive report CSV
            report_df = merged_df.copy()
            report_df['rhythm_score'] = results['rhythm_score']
            report_df['machine_score'] = results['machine_score']
            report_df['human_score'] = results['human_score']
            
            csv = report_df.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv,
                file_name=f"rhythm_report_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button("🔄 Re-analyze Data", use_container_width=True):
            st.session_state.page = 'upload'
            st.session_state.analysis_complete = False
            st.rerun()
    
    with col3:
        if st.button("📊 Back to Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()

# ==============================================================================
# MAIN APP ROUTER
# ==============================================================================

def main():
    """Main application router"""
    
    # Sidebar navigation (minimal)
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 2rem 0;'>
                <h2 style='background: linear-gradient(135deg, #00D9FF 0%, #FF6B9D 100%); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    🤖❤️
                </h2>
                <p style='color: #94a3b8; font-size: 0.9rem;'>Rhythm of the Machines</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("📤 Upload Data", use_container_width=True):
            st.session_state.page = 'upload'
            st.rerun()
        
        if st.session_state.analysis_complete:
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            if st.button("💡 Insights", use_container_width=True):
                st.session_state.page = 'insights'
                st.rerun()
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; color: #64748b; font-size: 0.75rem; padding: 1rem;'>
                <p>Built for Hackathon 2025</p>
                <p>Balance • Harmony • Rhythm</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if st.session_state.page == 'home':
        home_page()
    elif st.session_state.page == 'upload':
        upload_page()
    elif st.session_state.page == 'processing':
        processing_page()
    elif st.session_state.page == 'dashboard':
        dashboard_page()
    elif st.session_state.page == 'insights':
        insights_page()
    else:
        home_page()

# ==============================================================================
# RUN APPLICATION
# ==============================================================================

if __name__ == "__main__":
    main()