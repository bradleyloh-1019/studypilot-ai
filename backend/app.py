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

# 升级版 call_llm：支持接收图片数据
def call_llm(prompt: str, image_data: str = None, mime_type: str = None) -> str:
    if not GEMINI_API_KEY:
        return "GEMINI_API_KEY not set."

    url = (
        "https://generativelanguage.googleapis.com/v1/"
        f"models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    )

    parts = [{"text": prompt}]

    # 如果有图片，按照 Gemini 要求加入 payload
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
        response = requests.post(url, json=payload, timeout=30) # 图片处理可能稍慢，把超时改到30秒
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

    topic = data.get("topic", "").strip()
    mode = data.get("mode", "").strip()
    quiz_text = data.get("quizText", "").strip()
    
    # 接收前端传来的图片数据
    image_data = data.get("image_data")
    image_mime_type = data.get("image_mime_type")

    # 如果没有输入文字且没有图片，则拦截
    if not topic and not image_data:
        return jsonify({"result": "Please enter a topic or upload an image before continuing."})

    variation_id = int(time.time()) + random.randint(1, 9999)
    language_rule = "CRITICAL: Respond in the same language as the user's input.\n\n"

    # 如果用户只传了图片没写字，默认用 "this image" 替代 topic 防止报错
    safe_topic = topic if topic else "this image"

    if mode == "explain":
        system_prompt = get_agent_prompt("concept_explainer_agent.md")
        prompt = f"{system_prompt}\n\n{language_rule}Topic/Image to explain: {safe_topic}"

    elif mode == "quiz":
        system_prompt = get_agent_prompt("quiz_generator_agent.md")
        prompt = f"{system_prompt}\n\n{language_rule}Topic/Image: {safe_topic}\nVariation ID: {variation_id}"

    elif mode == "reveal":
        system_prompt = get_agent_prompt("quiz_generator_agent.md")
        if not quiz_text:
            return jsonify({"result": "Please attempt a quiz before revealing answers."})
        prompt = f"{system_prompt}\n\n{language_rule}Provide correct answers with brief explanations for this quiz:\n{quiz_text}"

    elif mode == "study":
        system_prompt = get_agent_prompt("study_feedback_agent.md")
        prompt = f"{system_prompt}\n\n{language_rule}Topic/Image: {safe_topic}"

    else:
        return jsonify({"result": "Invalid action selected."})

    # 将图片数据一起传给模型
    result = call_llm(prompt, image_data, image_mime_type)
    return jsonify({"result": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)