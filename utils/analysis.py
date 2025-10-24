
# ==============================================================================
# FILE 4: utils/analysis.py
# ==============================================================================

"""
AI analysis functions for rhythm score calculation and insights generation
"""

import pandas as pd
import numpy as np

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
    avg_work_hours = merged_df['work_hours'].mean()
    avg_tasks = merged_df['tasks_completed'].mean()
    machine_score = min(100, (avg_work_hours / 8 * 50 + avg_tasks / 10 * 50))
    
    avg_mood = merged_df['mood_score'].mean()
    avg_stress = merged_df['stress_level'].mean()
    avg_sleep = merged_df['sleep_hours'].mean()
    human_score = (avg_mood / 10 * 40 + (10 - avg_stress) / 10 * 30 + avg_sleep / 8 * 30)
    
    imbalance = abs(machine_score - human_score)
    balance_penalty = (imbalance / 100) * 20
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
    """AI-powered anomaly detection"""
    anomalies = []
    
    # Burnout risk
    burnout_days = merged_df[(merged_df['work_hours'] > 10) & (merged_df['mood_score'] < 5)]
    if len(burnout_days) > 0:
        anomalies.append({
            'type': 'danger',
            'title': 'Burnout Risk Detected',
            'description': f'{len(burnout_days)} days with 10+ work hours and mood below 5',
            'icon': '🚨'
        })
    
    # Sleep deficit
    sleep_deficit = merged_df[merged_df['sleep_hours'] < 6]
    if len(sleep_deficit) > 3:
        anomalies.append({
            'type': 'warning',
            'title': 'Sleep Deficit Pattern',
            'description': f'{len(sleep_deficit)} days with less than 6 hours of sleep',
            'icon': '😴'
        })
    
    # Positive trends
    if len(merged_df) > 7:
        recent_mood = merged_df.tail(7)['mood_score'].mean()
        earlier_mood = merged_df.head(7)['mood_score'].mean()
        if recent_mood > earlier_mood + 1:
            anomalies.append({
                'type': 'success',
                'title': 'Positive Mood Trend',
                'description': f'Mood improved by {round(recent_mood - earlier_mood, 1)} points',
                'icon': '✨'
            })
    
    # Overwork periods
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
    """AI-generated personalized insights"""
    insights = []
    merged_df = analysis_results['merged_data']
    correlation = analysis_results['correlation']
    
    # Peak productivity pattern
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
    
    # Work-wellbeing correlation
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
    
    # Sleep impact
    sleep_mood_corr = merged_df['sleep_hours'].corr(merged_df['mood_score'])
    if sleep_mood_corr > 0.4:
        insights.append({
            'icon': '😴',
            'title': 'Sleep is Your Superpower',
            'description': f'Strong link between sleep and mood (correlation: {sleep_mood_corr:.2f})',
            'recommendation': f'Prioritize {merged_df["sleep_hours"].quantile(0.75):.1f}+ hours of sleep for optimal wellbeing.',
            'color': 'human'
        })
    
    # Optimal work range
    optimal_work = merged_df[merged_df['mood_score'] >= 7]['work_hours'].median()
    insights.append({
        'icon': '🎯',
        'title': 'Your Sweet Spot Identified',
        'description': f'You maintain high mood (7+) with around {optimal_work:.1f} work hours per day',
        'recommendation': f'Target {optimal_work:.1f} hours as your baseline. Current adherence: {len(merged_df[abs(merged_df["work_hours"] - optimal_work) < 1]) / len(merged_df) * 100:.0f}%',
        'color': 'balance'
    })
    
    return insights

def generate_sample_data():
    """Generate sample data for testing"""
    dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
    
    work_data = pd.DataFrame({
        'date': dates,
        'work_hours': np.random.normal(8, 1.5, 30).clip(5, 12),
        'tasks_completed': np.random.poisson(10, 30),
        'server_uptime': np.random.uniform(98, 100, 30)
    })
    
    mood_data = pd.DataFrame({
        'date': dates,
        'mood_score': (10 - work_data['work_hours'] * 0.5 + np.random.normal(0, 1, 30)).clip(1, 10),
        'stress_level': (work_data['work_hours'] * 0.5 + np.random.normal(0, 1, 30)).clip(1, 10),
        'sleep_hours': (9 - work_data['work_hours'] * 0.2 + np.random.normal(0, 0.5, 30)).clip(5, 9)
    })
    
    return work_data, mood_data