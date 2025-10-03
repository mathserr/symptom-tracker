from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Create data directory if it doesn't exist
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

SYMPTOM_FILE = os.path.join(DATA_DIR, 'symptom_log.json')

def load_symptoms():
    """Load symptoms from JSON file"""
    try:
        with open(SYMPTOM_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_symptoms(data):
    """Save symptoms to JSON file"""
    with open(SYMPTOM_FILE, 'w') as f:
        json.dump(data, f, indent=2)

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

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)