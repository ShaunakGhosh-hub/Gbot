import os
import random
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv  # Import dotenv to load environment variables
from intents import intents  # Import intents from intents.py

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chat route
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    bot_response = get_bot_response(user_message)
    return jsonify({'response': bot_response})

# Function to process the user message
def get_bot_response(message):
    message = message.lower()
    
    # Check predefined intents
    for intent, values in intents.items():
        for pattern in values['patterns']:
            if pattern in message:
                return random.choice(values['responses'])
    
    # If no intent matches, fetch from Gemini API
    return fetch_from_gemini(message)

# Function to fetch response from Gemini API
def fetch_from_gemini(query):
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    api_key = os.getenv("GEMINI_API_KEY")  # Fetch API key from environment variables
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [{"parts": [{"text": query}]}]
    }

    try:
        # Send request to the API
        response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "I couldn't fetch the information you requested."

    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Gemini API: {e}")
        return "I'm having trouble accessing the web right now."

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
