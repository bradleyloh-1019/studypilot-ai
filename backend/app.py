from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  

OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "gemma"

def call_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API, json=payload)
    return response.json().get("response", "")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    topic = data.get("topic")
    mode = data.get("mode")

    if not topic or not mode:
        return jsonify({"error": "Missing topic or mode"}), 400

    if mode == "explain":
        prompt = f"Explain this topic simply for a diploma student:\n{topic}"
    elif mode == "quiz":
        prompt = f"Create 5 multiple-choice questions with answers on:\n{topic}"
    elif mode == "study":
        prompt = f"Give study tips and revision advice for:\n{topic}"
    else:
        return jsonify({"error": "Invalid mode"}), 400

    ai_result = call_llm(prompt)

    return jsonify({
        "topic": topic,
        "mode": mode,
        "result": ai_result
    })

if __name__ == "__main__":
    app.run(debug=True)