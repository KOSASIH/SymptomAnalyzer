from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Mock data for demonstration purposes
# In a real application, this would be replaced with actual model inference
conditions_database = {
    "headache": [
        {"condition": "Tension Headache", "probability": 0.8, "recommendation": "Rest, over-the-counter pain relievers, stress management"},
        {"condition": "Migraine", "probability": 0.6, "recommendation": "Rest in a dark room, prescription medications if severe"},
        {"condition": "Dehydration", "probability": 0.5, "recommendation": "Drink water, electrolyte solutions"}
    ],
    "fever": [
        {"condition": "Common Cold", "probability": 0.7, "recommendation": "Rest, fluids, over-the-counter fever reducers"},
        {"condition": "Influenza", "probability": 0.6, "recommendation": "Rest, fluids, antiviral medications if caught early"},
        {"condition": "COVID-19", "probability": 0.5, "recommendation": "Isolate, get tested, contact healthcare provider"}
    ],
    "cough": [
        {"condition": "Common Cold", "probability": 0.8, "recommendation": "Rest, fluids, over-the-counter cough suppressants"},
        {"condition": "Bronchitis", "probability": 0.5, "recommendation": "Rest, increased fluid intake, humidifier"},
        {"condition": "Asthma", "probability": 0.4, "recommendation": "Use prescribed inhalers, avoid triggers"}
    ],
    "fatigue": [
        {"condition": "Sleep Deprivation", "probability": 0.7, "recommendation": "Improve sleep habits, maintain regular sleep schedule"},
        {"condition": "Anemia", "probability": 0.5, "recommendation": "Iron-rich diet, supplements if recommended by doctor"},
        {"condition": "Depression", "probability": 0.4, "recommendation": "Consult mental health professional, regular exercise"}
    ]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_symptoms():
    data = request.json
    symptoms = data.get('symptoms', '').lower()
    
    # Simple keyword matching for demonstration
    # In a real application, this would use the Bio-Medical-MultiModal-Llama-3-8B model
    results = []
    for keyword in conditions_database:
        if keyword in symptoms:
            results.extend(conditions_database[keyword])
    
    # Sort by probability
    results = sorted(results, key=lambda x: x['probability'], reverse=True)
    
    # Remove duplicates
    unique_results = []
    seen_conditions = set()
    for result in results:
        if result['condition'] not in seen_conditions:
            unique_results.append(result)
            seen_conditions.add(result['condition'])
    
    response = {
        "input_symptoms": symptoms,
        "potential_conditions": unique_results[:5],  # Limit to top 5 results
        "disclaimer": "This is not medical advice. Please consult with a healthcare professional for accurate diagnosis."
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)