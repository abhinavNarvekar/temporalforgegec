# ==============================================================================
# FILE 2: utils/__init__.py
# ==============================================================================

# Empty file to make utils a package


# ==============================================================================
# FILE 3: utils/styling.py
# ==============================================================================

"""
Custom CSS styling for the application
"""

import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the application"""
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

