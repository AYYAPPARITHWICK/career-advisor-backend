# backend/app.py

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai  # Correct import

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in environment or .env before running")

# Set the API key
genai.api_key = GEMINI_API_KEY

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow frontend to access backend

@app.route("/")
def home():
    return "🚀 Career Advisor Backend is Live!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query") or data.get("message")

        if not query:
            return jsonify({"error": "Query or message is required"}), 400

        # Generate AI response for Quick Chat
        response = genai.chat.create(
            model="gemini-1.5",
            messages=[{"author": "user", "content": query}]
        )

        # Extract text from response
        text_response = response.last.message.get("content", "")

        return jsonify({"response": text_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        skills = data.get("skills", [])
        interests = data.get("interests", [])
        goal = data.get("goal", "")

        if not goal:
            return jsonify({"error": "Goal is required"}), 400

        # Build prompt for AI Skill Analysis
        prompt = f"""
I want to become a {goal}.
My current skills: {', '.join(skills) if skills else 'None'}
My interests: {', '.join(interests) if interests else 'None'}
Please provide a detailed roadmap and advice to achieve my goal.
"""

        # Generate AI response for Skill Analyzer
        response = genai.chat.create(
            model="gemini-1.5",
            messages=[{"author": "user", "content": prompt}]
        )

        advice_text = response.last.message.get("content", "")

        return jsonify({
            "skills": skills,
            "interests": interests,
            "goal": goal,
            "advice": advice_text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
