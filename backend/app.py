import os
import time
import random
import requests

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# =========================
# Environment Variables
# =========================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

IS_RENDER = os.getenv("RENDER") == "true"

# =========================
# Optional Supabase Setup
# =========================

supabase = None
if SUPABASE_URL and SUPABASE_ANON_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        print("Supabase connected")
    except Exception as e:
        print("Supabase not available:", e)

# =========================
# Flask App Setup
# =========================

app = Flask(__name__, static_folder="../frontend")
CORS(app)

# =========================
# Frontend Routes (关键)
# =========================

@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory("../frontend", path)

# =========================
# Ollama (Local Only)
# =========================

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "gemma"

def call_llm(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(
            OLLAMA_API,
            json=payload,
            timeout=120
        )
        return response.json().get("response", "")
    except Exception:
        return "Local AI engine is unavailable."

# =========================
# API Route
# =========================

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
        "Respond in the same language as the user's input. "
        "Do NOT mention language detection or analysis.\n\n"
    )

    if mode == "explain":
        prompt = (
            learner_assumption +
            language_rule +
            "You are acting as a tutor.\n"
            "Explain the following topic clearly and directly.\n\n"
            f"{topic}"
        )

    elif mode == "quiz":
        prompt = (
            learner_assumption +
            language_rule +
            "You are acting as an assessor.\n"
            "Generate exactly 5 multiple-choice questions.\n"
            "- 4 options (A–D)\n"
            "- No answers\n\n"
            f"{topic}"
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
            "You are acting as a study coach.\n"
            "Give study tips, common mistakes, and strategies.\n\n"
            f"{topic}"
        )

    else:
        return jsonify({"result": "Invalid action selected."})

    if IS_RENDER:
        result = (
            "This is the deployed demo version of StudyPilot AI.\n\n"
            "Full AI inference runs locally. "
            "This online version demonstrates the system flow and UI."
        )
    else:
        result = call_llm(prompt)

    return jsonify({"result": result})

# =========================
# App Entry Point
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
