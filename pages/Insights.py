"""
4_💡_Insights.py - AI-generated insights and recommendations page
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))
from utils.styling import apply_custom_css, render_gradient_header
from utils.analysis import generate_insights

# ============================================================================== 
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Insights - Rhythm of the Machines",
    page_icon="💡",
    layout="wide"
)

# Apply custom styling
apply_custom_css()

# ============================================================================== 
# CARD RENDER FUNCTION (DARK MODE FRIENDLY)
# ==============================================================================
def render_insight_card_dark(insight):
    """Render insight card with dark background and visible font."""
    return f"""
    <div style="
        background-color: rgba(50, 50, 50, 0.85);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        font-family: 'Arial', sans-serif;
    ">
        <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">
            💡 {insight['title']}
        </div>
        <div style="font-size: 1rem; color: #d1d5db;">
            {insight['description']}
        </div>
    </div>
    """

# ============================================================================== 
# MAIN INSIGHTS PAGE
# ==============================================================================
def main():
    """AI-generated insights and recommendations"""

    # Check if analysis is complete
    if 'rhythm_score' not in st.session_state or st.session_state.rhythm_score is None:
        st.error("⚠️ No analysis results found. Please upload and analyze data first.")
        if st.button("← Go to Upload Page"):
            st.switch_page("pages/1_📤_Upload_Data.py")
        return

    results = st.session_state.rhythm_score

    # Header
    render_gradient_header(
        "💡 AI-Generated Insights",
        "Personalized recommendations based on your rhythm analysis"
    )

    # Generate insights
    insights = generate_insights(results)

    # Display insights in a visually appealing two-column grid
    cols = st.columns(2)
    for idx, insight in enumerate(insights):
        with cols[idx % 2]:
            st.markdown(render_insight_card_dark(insight), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Historical Trends Section
    st.markdown("### 📊 Historical Rhythm Trends")
    merged_df = results['merged_data']

    # Weekly rhythm scores
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

    weekly_df = pd.DataFrame(weekly_scores)

    # Trend visualization
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
            <div style='text-align: center; padding: 2rem; background-color: rgba(50,50,50,0.85);
                        border-radius: 15px; margin-top: 2rem;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>{trend_emoji}</div>
                <p style='font-size: 1.3rem; color: {trend_color}; font-weight: bold;'>{trend_text}</p>
                <p style='color: #ffffff;'>{abs(trend):.1f} point {'increase' if trend > 0 else 'decrease'} from week 1 to week {len(weekly_scores)}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Weekly Breakdown
    st.markdown("### 📅 Weekly Performance Breakdown")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['machine'],
        name='Machine Score',
        line=dict(color='#00D9FF', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.3)'
    ))
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['human'],
        name='Human Score',
        line=dict(color='#FF6B9D', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 157, 0.3)'
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(21, 27, 59,0.5)",
        font={'color': "white"},
        yaxis=dict(title="Score", gridcolor='rgba(255,255,255,0.1)', range=[0,100]),
        xaxis=dict(title="Week", gridcolor='rgba(255,255,255,0.1)'),
        height=350,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Action buttons & download
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = merged_df.to_csv(index=False)
        st.download_button(
            "📥 Download Full Report",
            data=csv,
            file_name=f"rhythm_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    with col2:
        if st.button("🔄 Re-analyze Data", use_container_width=True):
            st.session_state.analysis_complete = False
            st.switch_page("pages/Upload_Data.py")

    with col3:
        if st.button("📊 Back to Dashboard", use_container_width=True):
            st.switch_page("pages/Dashboard.py")


if __name__ == "__main__":
    main()
