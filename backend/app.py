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

def call_llm(prompt: str, image_data: str = None, mime_type: str = None) -> str:
    if not GEMINI_API_KEY:
        return "GEMINI_API_KEY not set."

    url = (
        "https://generativelanguage.googleapis.com/v1/"
        f"models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    )

    parts = [{"text": prompt}]

    if image_data and mime_type:
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": image_data
            }
        })

    payload = {
        "contents": [{"parts": parts}]
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        data = response.json()

        if "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        if "error" in data:
            return f"Gemini error: {data['error'].get('message', 'Unknown error')}"

        return "Gemini did not return a response."
    except Exception as e:
        return f"Gemini request failed: {str(e)}"

def get_agent_prompt(filename: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
    filepath = os.path.join(base_dir, "agent", filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a helpful AI tutor."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json or {}

    topic = (data.get("topic") or "").strip()
    mode = (data.get("mode") or "").strip()
    quiz_text = (data.get("quizText") or "").strip()
    image_data = data.get("image_data")
    image_mime_type = data.get("image_mime_type")
    user_answers = (data.get("user_answers") or "").strip()

    if not topic and not image_data and mode != "grade":
        return jsonify({"result": "Please enter a topic or upload an image before continuing."})

    variation_id = int(time.time()) + random.randint(1, 9999)
    language_rule = "CRITICAL: Respond in the same language as the user's input.\n\n"
    safe_topic = topic if topic else "this image"

    if mode == "explain":
        system_prompt = get_agent_prompt("concept_explainer_agent.md")
        prompt = f"{system_prompt}\n\n{language_rule}Topic/Image to explain: {safe_topic}"

    elif mode == "quiz":
        system_prompt = get_agent_prompt("quiz_generator_agent.md")
        prompt = f"{system_prompt}\n\n{language_rule}CRITICAL INSTRUCTION: ONLY output the questions and options (A-D). DO NOT generate or reveal the answers or explanations at the bottom.\n\nTopic/Image: {safe_topic}\nVariation ID: {variation_id}"

    elif mode == "grade":
        system_prompt = get_agent_prompt("study_feedback_agent.md")
        if not quiz_text:
            return jsonify({"result": "Error: Quiz data missing."})
        prompt = (
            f"{system_prompt}\n\n{language_rule}"
            f"Here is the quiz the student just took:\n{quiz_text}\n\n"
            f"Here are the student's selected answers:\n{user_answers}\n\n"
            f"Please act as a strict but encouraging tutor. Grade the quiz. "
            f"Tell them their total score, point out which ones they got right/wrong, "
            f"and provide the correct answers with brief explanations for their mistakes."
        )

    elif mode == "study":
        system_prompt = get_agent_prompt("study_feedback_agent.md")
        prompt = f"{system_prompt}\n\n{language_rule}Topic/Image: {safe_topic}"

    else:
        return jsonify({"result": "Invalid action selected."})

    result = call_llm(prompt, image_data, image_mime_type)
    return jsonify({"result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)