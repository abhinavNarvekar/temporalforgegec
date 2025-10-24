# ==============================================================================
# FILE 7: pages/3_📊_Dashboard.py
# ==============================================================================

"""
Dashboard Page - Dark Full Page, No Sidebar
"""

import streamlit as st
import plotly.graph_objects as go
from utils.styling import apply_custom_css
from utils.analysis import detect_anomalies

# =========================
# Page config & CSS
# =========================
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
apply_custom_css()

# Hide sidebar menu & footer
st.markdown(
    """
    <style>
    /* Hide hamburger menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Full dark background */
    .css-18e3th9 {background-color: #0f111a;}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Check if analysis is complete
# =========================
if st.session_state.rhythm_score is None:
    st.error("No analysis results found. Please upload data first.")
    if st.button("← Back to Upload"):
        st.switch_page("pages/Upload_Data.py")
    st.stop()

results = st.session_state.rhythm_score
merged_df = results['merged_data']

# =========================
# Header
# =========================
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("""
        <h1 style='background: linear-gradient(135deg, #00D9FF 0%, #FF6B9D 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            📊 Your Rhythm Dashboard
        </h1>
    """, unsafe_allow_html=True)
    st.markdown(
        f"<p style='color: #94a3b8; font-size: 1.1rem;'>Analysis Period: {merged_df['date'].min().strftime('%b %d')} - {merged_df['date'].max().strftime('%b %d, %Y')}</p>",
        unsafe_allow_html=True
    )

with col2:
    if st.button("📥 Export Report"):
        csv = merged_df.to_csv(index=False)
        st.download_button(
            label="💾 Download CSV",
            data=csv,
            file_name=f"rhythm_report.csv",
            mime="text/csv"
        )

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# Central Rhythm Score
# =========================
st.markdown("""
<div style='text-align: center; padding: 3rem; 
            background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(255, 107, 157, 0.1) 100%);
            border-radius: 30px; margin-bottom: 2rem; box-shadow: 0 10px 40px rgba(183, 148, 246, 0.2);'>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    rhythm_score = results['rhythm_score']
    
    if rhythm_score >= 75:
        status, color = "Excellent", "#4ADE80"
    elif rhythm_score >= 60:
        status, color = "Balanced", "#B794F6"
    elif rhythm_score >= 45:
        status, color = "Moderate", "#FBBF24"
    else:
        status, color = "Needs Attention", "#F87171"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
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
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 75}
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"},
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

# =========================
# Stats Cards
# =========================
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
    corr_status = "Strong" if abs(results['correlation']) > 0.5 else "Moderate"
    st.metric(
        label="🔗 Correlation",
        value=results['correlation'],
        delta=corr_status
    )

# =========================
# Main Chart and Alerts
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📈 Productivity vs Wellbeing Trends")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=merged_df['date'],
        y=merged_df['work_hours'],
        name='Work Hours',
        line=dict(color='#00D9FF', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.1)'
    ))
    
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
        yaxis=dict(title="Work Hours", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="Mood Score", overlaying='y', side='right'),
        hovermode='x unified',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    insight_type = 'success' if results['correlation'] > 0 else 'warning'
    if results['correlation'] < -0.3:
        insight_msg = f"Strong negative correlation detected. When work hours increase, mood tends to decrease by {abs(results['correlation']) * 100:.0f}%."
    elif results['correlation'] > 0.3:
        insight_msg = "Positive correlation found. Your work energizes you when balanced properly."
    else:
        insight_msg = "Weak correlation between work hours and mood. Other factors may be more influential."
    
    st.markdown(f"""
        <div class='alert-{insight_type}'>
            <strong>🧠 AI Insight:</strong> {insight_msg}
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🚨 Active Alerts")
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
            st.markdown(f"""
                <div class='alert-{anomaly['type']}'>
                    <strong>{anomaly['icon']} {anomaly['title']}</strong><br>
                    <small>{anomaly['description']}</small>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("💡 View Detailed Insights", key="view_insights"):
        st.switch_page("pages/Insights.py")

# =========================
# Additional visualizations
# =========================
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔥 Work Intensity Heatmap")
    
    merged_df['day_of_week'] = merged_df['date'].dt.day_name()
    merged_df['week'] = merged_df['date'].dt.isocalendar().week
    
    pivot_data = merged_df.pivot_table(
        values='work_hours',
        index='day_of_week',
        columns='week',
        aggfunc='mean'
    )
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_data = pivot_data.reindex([day for day in day_order if day in pivot_data.index])
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=[f"Week {int(w)}" for w in pivot_data.columns],
        y=pivot_data.index,
        colorscale=[[0, '#1a1f4d'], [0.5, '#B794F6'], [1, '#00D9FF']],
        text=pivot_data.values.round(1),
        texttemplate='%{text}h',
        textfont={"size": 10}
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
    
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=merged_df['mood_score'],
        name='Mood Score',
        marker_color='#FF6B9D',
        boxmean='sd'
    ))
    
    fig.add_trace(go.Box(
        y=10 - merged_df['stress_level'],
        name='Low Stress',
        marker_color='#B794F6',
        boxmean='sd'
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(21, 27, 59, 0.5)",
        font={'color': "white"},
        yaxis=dict(title="Score (1-10)", gridcolor='rgba(255,255,255,0.1)', range=[0, 11]),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
