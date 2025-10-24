"""
4_💡_Insights.py - AI-generated insights and recommendations page
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path to import utils
sys.path.append(str(Path(__file__).parent.parent))
from utils.styling import apply_custom_css, render_gradient_header, render_insight_card
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
    
    # Display insights in a grid
    cols = st.columns(2)
    for idx, insight in enumerate(insights):
        with cols[idx % 2]:
            st.markdown(render_insight_card(insight), unsafe_allow_html=True)
    
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
    
    # Weekly Breakdown Section
    st.markdown("### 📅 Weekly Performance Breakdown")
    
    # Create a comparison chart for machine vs human scores by week
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['machine'],
        name='Machine Score',
        line=dict(color='#00D9FF', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['human'],
        name='Human Score',
        line=dict(color='#FF6B9D', width=3),
        fill='tozeroy',
        fillcolor='rgba(255, 107, 157, 0.2)'
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(21, 27, 59, 0.5)",
        font={'color': "white"},
        yaxis=dict(title="Score", gridcolor='rgba(255,255,255,0.1)', range=[0, 100]),
        xaxis=dict(title="Week", gridcolor='rgba(255,255,255,0.1)'),
        height=350,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Balance analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_machine = weekly_df['machine'].mean()
        st.markdown(f"""
            <div style='padding: 1.5rem; background: rgba(0, 217, 255, 0.1); 
                        border-radius: 15px; text-align: center;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🤖</div>
                <div style='color: #00D9FF; font-size: 2rem; font-weight: bold;'>{avg_machine:.1f}</div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>Avg Machine Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_human = weekly_df['human'].mean()
        st.markdown(f"""
            <div style='padding: 1.5rem; background: rgba(255, 107, 157, 0.1); 
                        border-radius: 15px; text-align: center;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>❤️</div>
                <div style='color: #FF6B9D; font-size: 2rem; font-weight: bold;'>{avg_human:.1f}</div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>Avg Human Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        balance_diff = abs(avg_machine - avg_human)
        balance_status = "Excellent" if balance_diff < 10 else "Good" if balance_diff < 20 else "Needs Work"
        balance_color = "#4ADE80" if balance_diff < 10 else "#FBBF24" if balance_diff < 20 else "#F87171"
        
        st.markdown(f"""
            <div style='padding: 1.5rem; background: rgba(183, 148, 246, 0.1); 
                        border-radius: 15px; text-align: center;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>⚖️</div>
                <div style='color: {balance_color}; font-size: 2rem; font-weight: bold;'>{balance_status}</div>
                <div style='color: #94a3b8; font-size: 0.9rem;'>Balance Status</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Actionable Recommendations Section
    st.markdown("### 🎯 Action Plan for Next Week")
    
    # Generate personalized action items based on the data
    action_items = []
    
    # Check work hours
    if results['avg_work_hours'] > 9:
        action_items.append({
            'priority': 'high',
            'icon': '⏰',
            'title': 'Reduce Work Hours',
            'action': f"Target {results['avg_work_hours'] - 1:.1f} hours/day (current: {results['avg_work_hours']:.1f}h)",
            'impact': 'High impact on stress reduction'
        })
    
    # Check sleep
    if results['avg_sleep'] < 7:
        action_items.append({
            'priority': 'high',
            'icon': '😴',
            'title': 'Prioritize Sleep',
            'action': f"Aim for 7.5+ hours nightly (current: {results['avg_sleep']:.1f}h)",
            'impact': 'Critical for mood and productivity'
        })
    
    # Check mood trends
    if results['avg_mood'] < 7:
        action_items.append({
            'priority': 'medium',
            'icon': '😊',
            'title': 'Boost Wellbeing',
            'action': 'Schedule 30min daily for activities you enjoy',
            'impact': 'Improves overall life satisfaction'
        })
    
    # Check stress
    if results['avg_stress'] > 6:
        action_items.append({
            'priority': 'high',
            'icon': '🧘',
            'title': 'Stress Management',
            'action': 'Implement daily mindfulness or exercise routine',
            'impact': 'Reduces stress by 20-30%'
        })
    
    # Add a positive action
    action_items.append({
        'priority': 'medium',
        'icon': '📊',
        'title': 'Track Progress',
        'action': 'Continue logging metrics daily for pattern recognition',
        'impact': 'Enables data-driven optimization'
    })
    
    # Display action items
    for item in action_items:
        priority_color = '#F87171' if item['priority'] == 'high' else '#FBBF24'
        priority_label = '🔴 High Priority' if item['priority'] == 'high' else '🟡 Medium Priority'
        
        st.markdown(f"""
            <div style='padding: 1.5rem; background: rgba(183, 148, 246, 0.05); 
                        border-left: 4px solid {priority_color}; border-radius: 10px; 
                        margin-bottom: 1rem;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;'>
                    <div style='font-size: 1.5rem;'>{item['icon']} <strong style='color: white;'>{item['title']}</strong></div>
                    <div style='color: {priority_color}; font-size: 0.8rem;'>{priority_label}</div>
                </div>
                <div style='color: #cbd5e1; margin-bottom: 0.5rem;'>{item['action']}</div>
                <div style='color: #94a3b8; font-size: 0.85rem;'>💡 {item['impact']}</div>
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
            st.session_state.analysis_complete = False
            st.switch_page("pages/Upload_Data.py")
    
    with col3:
        if st.button("📊 Back to Dashboard", use_container_width=True):
            st.switch_page("pages/Dashboard.py")

if __name__ == "__main__":

    main()