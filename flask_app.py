#!/usr/bin/python3.10

"""
WSGI config for PythonAnywhere deployment
This file should be named flask_app.py in your PythonAnywhere files

For PythonAnywhere deployment:
1. Upload all your files to /home/mathserr/mysite/
2. Set up Web App with manual configuration (Python 3.10)
3. Point WSGI configuration to this file
"""

import sys
import os

# Add your project directory to Python path
path = '/home/mathserr/mysite'  # Replace 'mathserr' with your actual username
if path not in sys.path:
    sys.path.append(path)

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Use absolute paths for PythonAnywhere
BASE_DIR = '/home/mathserr/mysite'  # Replace 'mathserr' with your actual username
DATA_DIR = os.path.join(BASE_DIR, 'data')
SYMPTOM_FILE = os.path.join(DATA_DIR, 'symptom_log.json')

# Ensure data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def load_symptoms():
    """Load symptoms from JSON file"""
    try:
        with open(SYMPTOM_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_symptoms(data):
    """Save symptoms to JSON file"""
    try:
        with open(SYMPTOM_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        # Log error for debugging
        with open(os.path.join(BASE_DIR, 'error.log'), 'a') as f:
            f.write(f"{datetime.now()}: Error saving symptoms: {str(e)}\n")
        raise

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get symptoms for a specific date"""
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    data = load_symptoms()
    return jsonify(data.get(date, []))

@app.route('/api/symptoms', methods=['POST'])
def save_symptoms_api():
    """Save symptoms for a specific date"""
    try:
        request_data = request.get_json()
        date = request_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        symptoms = request_data.get('symptoms', [])
        
        data = load_symptoms()
        
        # Create entry with timestamp
        entry = {
            "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "symptoms": symptoms
        }
        
        # Replace existing entry for the same date
        data[date] = [entry]
        
        save_symptoms(data)
        
        return jsonify({"success": True, "message": "Symptoms saved successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/all-dates', methods=['GET'])
def get_all_dates():
    """Get all dates with symptom entries"""
    data = load_symptoms()
    return jsonify(list(data.keys()))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "data_file_exists": os.path.exists(SYMPTOM_FILE),
        "base_dir": BASE_DIR
    })

# This is required for PythonAnywhere
application = app

if __name__ == '__main__':
    app.run(debug=True)