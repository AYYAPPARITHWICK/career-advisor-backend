# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in environment or .env before running")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow frontend JS to call backend

@app.route("/")
def home():
    return "Career Advisor Backend with Gemini API is Running ✅"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        query = data.get("query") or data.get("message")

        if not query:
            return jsonify({"error": "Query or message is required"}), 400

        # Generate AI response for Quick Chat
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=query
        )

        return jsonify({"response": response.text})
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
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        return jsonify({
            "skills": skills,
            "interests": interests,
            "goal": goal,
            "advice": response.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
