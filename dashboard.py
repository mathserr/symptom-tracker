#!/usr/bin/python3.10

"""
Dashboard module for Symptom Tracker
Contains all functions related to data analysis and dashboard functionality
"""

import json
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import os

def load_symptoms_data(symptom_file):
    """Load symptoms from JSON file"""
    try:
        with open(symptom_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def get_dashboard_stats(data):
    """Calculate dashboard statistics from symptom data"""
    if not data:
        return {
            'total_entries': 0,
            'date_range': {'start': None, 'end': None},
            'symptom_frequency': {},
            'cycle_day_patterns': {},
            'recent_entries': [],
            'monthly_summary': {}
        }
    
    # Basic stats
    total_entries = len(data)
    dates = sorted(data.keys())
    date_range = {
        'start': dates[0] if dates else None,
        'end': dates[-1] if dates else None
    }
    
    # Symptom frequency analysis
    all_symptoms = []
    cycle_days = []
    recent_entries = []
    
    for date, entries in data.items():
        if entries:  # entries is a list
            latest_entry = entries[-1]  # Get the latest entry for that date
            symptoms = latest_entry.get('symptoms', [])
            cycle_day = latest_entry.get('cycleDay')
            comment = latest_entry.get('comment', '')
            datetime_str = latest_entry.get('datetime', date)
            
            # Process symptoms for frequency
            for symptom in symptoms:
                all_symptoms.append(symptom)
            
            # Track cycle days
            if cycle_day is not None:
                cycle_days.append(cycle_day)
            
            # Recent entries (last 7 days)
            try:
                entry_date = datetime.strptime(date, '%Y-%m-%d')
                if (datetime.now() - entry_date).days <= 7:
                    recent_entries.append({
                        'date': date,
                        'symptoms': symptoms,
                        'cycle_day': cycle_day,
                        'comment': comment,
                        'datetime': datetime_str
                    })
            except ValueError:
                pass
    
    # Calculate symptom frequency
    symptom_counter = Counter(all_symptoms)
    symptom_frequency = dict(symptom_counter.most_common())
    
    # Cycle day patterns
    cycle_day_patterns = {}
    if cycle_days:
        cycle_counter = Counter(cycle_days)
        cycle_day_patterns = {
            'most_common': cycle_counter.most_common(5),
            'average': sum(cycle_days) / len(cycle_days),
            'range': {'min': min(cycle_days), 'max': max(cycle_days)}
        }
    
    # Monthly summary
    monthly_data = defaultdict(lambda: {'entries': 0, 'symptoms': []})
    for date in dates:
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            month_key = date_obj.strftime('%Y-%m')
            monthly_data[month_key]['entries'] += 1
            
            # Add symptoms for this month
            if data[date]:
                latest_entry = data[date][-1]
                symptoms = latest_entry.get('symptoms', [])
                monthly_data[month_key]['symptoms'].extend(symptoms)
        except ValueError:
            continue
    
    # Process monthly symptoms
    monthly_summary = {}
    for month, month_data in monthly_data.items():
        symptom_count = Counter(month_data['symptoms'])
        monthly_summary[month] = {
            'entries': month_data['entries'],
            'total_symptoms': len(month_data['symptoms']),
            'unique_symptoms': len(symptom_count),
            'top_symptoms': symptom_count.most_common(3)
        }
    
    # Sort recent entries by date (newest first)
    recent_entries.sort(key=lambda x: x['date'], reverse=True)
    
    return {
        'total_entries': total_entries,
        'date_range': date_range,
        'symptom_frequency': symptom_frequency,
        'cycle_day_patterns': cycle_day_patterns,
        'recent_entries': recent_entries[:7],  # Limit to 7 most recent
        'monthly_summary': dict(sorted(monthly_summary.items(), reverse=True))
    }

def get_symptom_trends(data, symptom_name):
    """Get trend data for a specific symptom over time"""
    trend_data = []
    
    for date, entries in sorted(data.items()):
        if entries:
            latest_entry = entries[-1]
            symptoms = latest_entry.get('symptoms', [])
            cycle_day = latest_entry.get('cycleDay')
            
            # Check if symptom occurred
            occurred = any(symptom_name.lower() in symptom.lower() for symptom in symptoms)
            
            trend_data.append({
                'date': date,
                'occurred': occurred,
                'cycle_day': cycle_day,
                'all_symptoms': symptoms
            })
    
    return trend_data

def get_cycle_analysis(data):
    """Analyze patterns based on cycle days"""
    cycle_symptom_map = defaultdict(list)
    
    for date, entries in data.items():
        if entries:
            latest_entry = entries[-1]
            cycle_day = latest_entry.get('cycleDay')
            symptoms = latest_entry.get('symptoms', [])
            
            if cycle_day is not None:
                cycle_symptom_map[cycle_day].extend(symptoms)
    
    # Calculate symptom frequency per cycle day
    cycle_analysis = {}
    for cycle_day, symptoms in cycle_symptom_map.items():
        symptom_counter = Counter(symptoms)
        cycle_analysis[cycle_day] = {
            'total_occurrences': len(symptoms),
            'symptom_frequency': dict(symptom_counter),
            'most_common_symptom': symptom_counter.most_common(1)[0] if symptom_counter else None
        }
    
    return dict(sorted(cycle_analysis.items()))