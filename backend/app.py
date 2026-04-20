import os
import time
import random
import requests

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = Flask(__name__, static_folder="../frontend")
CORS(app)

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)

def call_llm(prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "GEMINI_API_KEY not set."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, json=payload, timeout=20)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini error: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}

    topic = data.get("topic", "").strip()
    mode = data.get("mode", "").strip()
    quiz_text = data.get("quizText", "").strip()

    if not topic:
        return jsonify({"result": "Please enter a topic before continuing."})

    variation_id = int(time.time()) + random.randint(1, 9999)

    learner_assumption = (
        "The AI assumes the user is a student preparing for assessments or exams.\n\n"
    )

    language_rule = (
        "Respond in the same language as the user's input.\n\n"
    )

    if mode == "explain":
        prompt = (
            learner_assumption +
            language_rule +
            "Explain the following topic clearly for exams.\n\n"
            f"{topic}"
        )

    elif mode == "quiz":
        prompt = (
            learner_assumption +
            language_rule +
            "Generate exactly 5 multiple-choice questions.\n"
            "Options A to D.\n"
            "Do not show answers.\n\n"
            f"Topic: {topic}\n"
            f"Variation ID: {variation_id}"
        )

    elif mode == "reveal":
        if not quiz_text:
            return jsonify({"result": "Please attempt a quiz before revealing answers."})
        prompt = (
            learner_assumption +
            language_rule +
            "Provide correct answers with brief explanations.\n\n"
            f"{quiz_text}"
        )

    elif mode == "study":
        prompt = (
            learner_assumption +
            language_rule +
            "Give study tips, common mistakes, and revision strategies.\n\n"
            f"{topic}"
        )

    else:
        return jsonify({"result": "Invalid action selected."})

    result = call_llm(prompt)
    return jsonify({"result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)