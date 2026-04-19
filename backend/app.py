import os
import time
import random
import requests

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# =========================
# Environment Setup
# =========================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Render 会自动注入这个环境变量
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

app = Flask(__name__)
CORS(app)

# =========================
# Ollama (Local Only)
# =========================

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "gemma"

def call_llm(prompt: str) -> str:
    """
    Local LLM call (Ollama).
    This will ONLY be used in local development.
    """
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
        return jsonify({
            "result": "Please enter a topic before continuing."
        })

    variation_id = int(time.time()) + random.randint(1, 9999)

    learner_assumption = (
        "The AI assumes the user is a student preparing for assessments or exams.\n\n"
    )

    language_rule = (
        "Respond in the same language as the user's input. "
        "Do NOT mention language detection or analysis.\n\n"
    )

    # -------------------------------
    # Build Prompt
    # -------------------------------

    if mode == "explain":
        prompt = (
            learner_assumption +
            language_rule +
            "You are acting as a tutor.\n"
            "Explain the following topic clearly and directly, "
            "focusing on exam-relevant understanding.\n\n"
            f"{topic}"
        )

    elif mode == "quiz":
        prompt = (
            learner_assumption +
            language_rule +
            "You are acting as an assessor.\n"
            "Generate assessment questions to test understanding "
            "of the following subject.\n\n"
            f"Topic:\n{topic}\n"
            f"Variation ID: {variation_id}\n\n"
            "Generate exactly 5 multiple-choice questions.\n"
            "- Each question has 4 options (A, B, C, D)\n"
            "- DO NOT include answers\n"
            "- DO NOT include explanations\n"
            "Output questions only."
        )

    elif mode == "reveal":
        if not quiz_text:
            return jsonify({
                "result": "Please attempt a quiz before revealing the answers."
            })

        prompt = (
            learner_assumption +
            language_rule +
            "You are providing delayed feedback.\n"
            "Based on the quiz questions below, provide the correct answers "
            "with brief explanations.\n\n"
            f"{quiz_text}"
        )

    elif mode == "study":
        prompt = (
            learner_assumption +
            language_rule +
            "You are acting as a study coach.\n"
            "Provide practical revision advice for the following subject.\n\n"
            f"{topic}\n\n"
            "- Key concepts to focus on\n"
            "- Common exam-related mistakes\n"
            "- Effective revision strategies"
        )

    else:
        return jsonify({
            "result": "Invalid action selected."
        })

    # -------------------------------
    # Response Logic
    # -------------------------------

    if IS_RENDER:
        # Online demo mode (no Ollama)
        result = (
            "This is the deployed demo version of StudyPilot AI.\n\n"
            "Full AI inference runs locally using a locally hosted LLM. "
            "This online version demonstrates the system flow and user interface."
        )
    else:
        # Local development mode (real LLM)
        result = call_llm(prompt)

    return jsonify({
        "result": result
    })

# =========================
# App Entry Point (Render Safe)
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)