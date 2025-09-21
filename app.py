# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import the latest google generative AI
import google.generativeai as genai

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return "🚀 Career Advisor Backend is Live!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Use generate_content method (correct approach)
        response = model.generate_content(query)
        
        # Handle response properly - response.text is the correct attribute
        text = response.text if hasattr(response, 'text') else str(response)
        
        return jsonify({"response": text})
    except Exception as e:
        return jsonify({"error": f"Backend error: {str(e)}"}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    skills = data.get("skills", [])
    interests = data.get("interests", [])
    goal = data.get("goal", "").strip()

    if not goal:
        return jsonify({"error": "No goal provided"}), 400

    try:
        prompt = f"""
        A user has the following skills: {', '.join(skills) if skills else 'None specified'}
        Interests: {', '.join(interests) if interests else 'None specified'}
        Goal: {goal}

        Analyze their skill gaps and provide personalized career advice in a concise manner.
        Include specific skills they should learn and career paths they could pursue.
        """

        response = model.generate_content(prompt)
        
        # Handle response properly - response.text is the correct attribute
        advice_text = response.text if hasattr(response, 'text') else str(response)
        
        return jsonify({"advice": advice_text})
    except Exception as e:
        return jsonify({"error": f"Backend error: {str(e)}"}), 500

if __name__ == "__main__":
    # Run backend on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)