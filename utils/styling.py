"""
styling.py - CSS styling and UI components for Rhythm of the Machines
"""

import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
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

def render_gradient_header(title, subtitle=None):
    """Render a gradient header (subtitle removed for Insights page)"""
    html = f"""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='font-size: 3.5rem; background: linear-gradient(135deg, #00D9FF 0%, #B794F6 50%, #FF6B9D 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;'>{title}</h1>
        </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_feature_card(icon, title, description, color="balance"):
    """Render a feature highlight card"""
    color_map = {
        "machine": "#00D9FF",
        "human": "#FF6B9D",
        "balance": "#B794F6"
    }
    
    card_color = color_map.get(color, color_map["balance"])
    
    return f"""
        <div style='text-align: center; padding: 1.5rem; background: rgba({
            '0, 217, 255' if color == 'machine' else 
            '255, 107, 157' if color == 'human' else 
            '183, 148, 246'
        }, 0.1); 
                    border-radius: 15px; margin: 1rem 0;'>{icon}</div>
            <div style='font-weight: bold; color: {card_color}; margin-top: 0.5rem;'>{title}</div>
            <div style='color: #94a3b8; font-size: 0.9rem;'>{description}</div>
        </div>
    """

def render_alert_box(alert_type, title, description, icon=""):
    """Render an alert box with specified type"""
    alert_class = f"alert-{alert_type}"
    
    return f"""
        <div class='{alert_class}'>
            <strong>{icon} {title}</strong><br>
            <small>{description}</small>
        </div>
    """

def render_insight_card(insight):
    """Render an insight card with recommendations"""
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
    
    return f"""
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
    """

def render_metric_card(label, value, delta=None):
    """Render a custom metric card"""
    delta_html = ""
    if delta:
        delta_color = "#4ADE80" if "+" in str(delta) else "#F87171"
        delta_html = f"<div style='color: {delta_color}; font-size: 0.9rem;'>{delta}</div>"
    
    return f"""
        <div style='padding: 1.5rem; background: rgba(183, 148, 246, 0.1); 
                    border-radius: 15px; text-align: center;'>
            <div style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;'>{label}</div>
            <div style='font-size: 2rem; font-weight: bold; color: white;'>{value}</div>
            {delta_html}
        </div>
    """

def render_sidebar():
    """Render the sidebar navigation"""
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
    
    st.markdown("""
        <div style='text-align: center; color: #64748b; font-size: 0.75rem; padding: 1rem;'>
            <p>Built for Hackathon 2025</p>
            <p>Balance • Harmony • Rhythm</p>
        </div>
    """, unsafe_allow_html=True)

def render_score_gauge_layout(rhythm_score, machine_score, human_score):
    """Render the layout for the central rhythm score gauge"""
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
    
    return {
        'status': status,
        'color': color,
        'html_wrapper_start': """
            <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(255, 107, 157, 0.1) 100%); 
                        border-radius: 30px; margin-bottom: 2rem; box-shadow: 0 10px 40px rgba(183, 148, 246, 0.2);'>
        """,
        'html_wrapper_end': "</div>",
        'component_scores_html': f"""
            <div style='display: flex; justify-content: center; gap: 3rem; margin-top: 2rem;'>
                <div style='text-align: center;'>
                    <div style='color: #00D9FF; font-size: 2rem; font-weight: bold;'>🤖 {machine_score}</div>
                    <div style='color: #94a3b8;'>Machine Score</div>
                </div>
                <div style='text-align: center;'>
                    <div style='color: #FF6B9D; font-size: 2rem; font-weight: bold;'>❤️ {human_score}</div>
                    <div style='color: #94a3b8;'>Human Score</div>
                </div>
            </div>
        """
    }
