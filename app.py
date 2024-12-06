import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("AIzaSyDcyDafeT1zCBhOQUubXm-2D-1jKtZPrjg"))  # Ensure your .env file contains API_KEY=your-api-key
                                  # update API key in .env file
# Initialize Flask app
app = Flask(__name__)

# Define model configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Imagine you are a friendly, knowledgeable, and conversational chatbot assistant."
)

# Start chat session
chat_session = model.start_chat(history=[])

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle user messages and get responses
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    response = chat_session.send_message(user_message)
    bot_response = response.text.replace("*", "").strip()
    
    # Append to history
    chat_session.history.append({"role": "user", "parts": [user_message]})
    chat_session.history.append({"role": "model", "parts": [bot_response]})
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
