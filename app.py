import random
import requests
from flask import Flask, request, jsonify, render_template
from intents import intents  # Import intents from intents.py

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chat route to handle user messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')  # Get user input from the request
    bot_response = get_bot_response(user_message)  # Process the message
    return jsonify({'response': bot_response})  # Return the chatbot response

# Function to process user message
def get_bot_response(message):
    message = message.lower()

    # Check predefined intents first
    for intent, values in intents.items():
        for pattern in values['patterns']:
            if pattern in message:
                return random.choice(values['responses'])  # Return a predefined response

    # If no intent matches, fetch from Gemini API
    return fetch_from_gemini(message)

# Function to fetch response from Google Gemini API
def fetch_from_gemini(query):
    api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "contents": [{"parts": [{"text": query}]}]
    }
    api_key = "AIzaSyBbvFQkWxyI2rtrlvBIQ7wGQzQlBW1pPtY"  

    try:
        # Send the POST request to Gemini API
        response = requests.post(f"{api_url}?key={api_key}", json=payload, headers=headers)
        response.raise_for_status()  # Raise an error if status code is not 2xx

        # Parse and process the response
        data = response.json()
        print("Response:", data)  # Log the response for debugging

       if "candidates" in data:
    return data["candidates"][0]["content"]["parts"][0].get("text", "")
        else:
            return "I'm sorry, I couldn't fetch the information you need."

    except requests.exceptions.RequestException as e:
        print("Error while fetching from Gemini API:", e)
        return "I'm having trouble accessing the web right now."

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
