# StudyPilot AI 🚀
Your Smart AI Learning Assistant

![Python](https://img.shields.io/badge/python-3.11-blue)
![Backend](https://img.shields.io/badge/backend-flask-black)
![AI Model](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)
![Feature](https://img.shields.io/badge/Feature-Multimodal%20Vision-purple)

## 🏆 Hackathon Context: Project 2030 MyAI Future

* **National Track Alignment:** Smart Education & Digital Inclusivity
* **Malaysia's National Digital Agenda:** StudyPilot AI supports the national vision of democratising digital education. By providing an advanced, accessible AI tutor capable of multimodal analysis and automated grading, it bridges the educational resource gap, empowering Malaysian students from diverse backgrounds with hyper-personalised learning tools.

---

## 📘 Project Overview

StudyPilot AI is an advanced, multimodal AI-powered learning assistant designed to support students in understanding complex academic concepts, assessing their knowledge, and improving exam preparation.

Unlike standard Q&A chatbots, StudyPilot AI functions as a complete educational ecosystem. It guides learners through a structured workflow: visual/textual concept explanation, dynamic self-testing, interactive automated grading, and targeted study advice.

---

## 🎯 Target Users & Learning Assumption

**The system assumes the user is a student preparing for assessments or examinations at secondary, pre-university, or diploma level.**

This learner assumption is embedded via carefully engineered Agent Prompts into the backend AI logic, influencing:
- The tone and depth of explanations.
- The structure and difficulty of generated multiple-choice questions.
- The strictness and encouragement level of the automated grading system.
- The nature of study advice provided.

## ❓ Problem Statement

Many students struggle with:
- Understanding abstract or unfamiliar academic concepts from textbooks, charts, or diagrams.
- Identifying gaps in their own knowledge through effective self-assessment.
- Receiving immediate, highly personalized feedback after attempting practice questions.
- Structuring efficient exam revision strategies.

Most AI tools act as simple Q&A bots that spoon-feed answers, short-circuiting the learning process. StudyPilot AI addresses this gap by integrating state-of-the-art multimodal AI into a structured educational workflow that encourages active learning, critical thinking, and reflection.

---

## ✅ Core Features

### 1. Explain Concept (Multimodal Tutor)
- **Text & Vision Support:** Users can type a topic or **upload an image** (e.g., a complex math formula, a science diagram, or a textbook page).
- Explains academic topics clearly, tailoring the depth for exam-oriented learning.
- Automatically responds in the language of the user's input.

### 2. Generate Quiz (Dynamic Assessor)
- Generates 5 assessment-style multiple-choice questions based on the text or uploaded image.
- Focuses on testing conceptual understanding rather than simple memorization.
- **Anti-Cheat Design:** Answers and explanations are strictly hidden during the generation phase to encourage genuine self-attempt.

### 3. Submit & Auto-Grade (Interactive Feedback)
- Replaces static "reveal answers" with an interactive grading system.
- Users select their answers via radio buttons directly on the interface and click "Submit & Grade Quiz".
- The AI strictly evaluates the submission, calculates the total score, highlights specific mistakes, and provides targeted, encouraging explanations to correct misunderstandings.

### 4. Study Tips (AI Study Coach)
- Analyzes the topic or uploaded material to identify key concepts for targeted revision.
- Highlights common exam-related mistakes and pitfalls.
- Suggests practical, highly effective revision strategies.

---

## 🧠 Educational Design Principles

StudyPilot AI is designed around established learning principles:

* **Multimodal Learning**: Supporting both textual and visual inputs caters to different learning materials and cognitive styles.
* **Active Recall & Testing Effect**: Learners must actively retrieve information to answer quiz questions before receiving correct answers, which significantly improves retention.
* **Targeted Interleaved Feedback**: Separating quiz attempts from answer explanations, and providing specific feedback on wrong choices, prevents the illusion of competence.
* **Learning Stage Awareness**: The AI dynamically switches roles (Tutor → Assessor → Coach) depending on the user's current phase in the learning cycle.

## 🏗 System Architecture

StudyPilot AI follows a modern client–server architecture integrated with Google's state-of-the-art cloud AI services.

### High-Level Architecture Overview

`User` ↓ `Frontend (HTML / CSS / JS)` ↓ `Backend API (Flask)` ↓ `Google Gemini API (Gemini 2.5 Flash)`

### Architecture Diagram

```mermaid
graph TD
U[User]
F[Frontend UI<br/>HTML / CSS / Vanilla JS]
B[Backend API<br/>Flask app.py]
G[Google Gemini API<br/>Gemini 2.5 Flash Multimodal]

U-->|Input Text & Upload Image|F
F-->|HTTP POST Request<br/>JSON + Base64 Image|B
B-->|System Prompt + Multimodal Payload|G
G-->|Generated Text / Markdown|B
B-->|Parsed Response|F

This diagram represents a scalable, cloud-connected system. The frontend manages user interaction and image preprocessing, the backend enforces learning logic and securely handles API communication, and the Gemini API handles complex multimodal inference.

---

## 🔧 Component-Level Architecture

### 1. Frontend (HTML / CSS / JavaScript)
The frontend is responsive, lightweight, and built without heavy frameworks to ensure maximum accessibility. Its responsibilities include:
- Capturing textual input and **processing image uploads** (converting images to Base64).
- Sending payloads (Topic + Mode + Image Data + User Answers) to the backend.
- Parsing and rendering AI-generated Markdown (using `marked.js`) for highly readable academic text.
- Dynamically generating interactive quiz forms and capturing user selections for the auto-grading system.

### 2. Backend API (Flask – `app.py`)
The Flask backend serves as the core control layer and security gatekeeper. It is responsible for:
- Receiving and validating requests from the frontend.
- **Dynamic Prompt Engineering:** Reading carefully crafted markdown files from the `/agent` directory to assign specific "personas" (Explainer, Assessor, Coach) to the AI.
- Formatting multimodal payloads (merging user text, Base64 images, and system instructions) to comply with the Google Gemini API structure.
- Securing the `GEMINI_API_KEY` (preventing exposure to the client-side).

### 3. AI Model: Google Gemini 2.5 Flash
StudyPilot AI leverages **Gemini 2.5 Flash** due to its exceptional speed and native multimodal capabilities. It is responsible for:
- Performing complex visual reasoning (e.g., extracting text from uploaded textbook pages, interpreting scientific diagrams).
- Generating structured educational content, adaptive quizzes, and empathetic, strict grading feedback.

---

## 🔄 Detailed Execution Flow (Example: Auto-Grading)

1. The user attempts a generated quiz on the frontend, selecting options via radio buttons.
2. The user clicks "Submit & Grade Quiz". The frontend captures the selected answers (or flags skipped questions).
3. The frontend sends a JSON payload containing the original quiz text and the user's answers to the backend under the `grade` mode.
4. The backend loads the `study_feedback_agent.md` system prompt.
5. The backend constructs a highly specific instruction, combining the system prompt, the original quiz, and the student's submission.
6. The payload is sent securely to the **Gemini 2.5 Flash API**.
7. Gemini evaluates the submission, calculates the score, and generates targeted explanations for incorrect answers.
8. The backend returns this feedback to the frontend, which parses the Markdown and displays the interactive, personalized tutoring response.

## 🚀 Live Demo & Deployment

The application is professionally hosted on **Render**, providing a seamless, zero-installation experience for students and educators.

### 🌐 Access the Web App
**[Click Here to Open StudyPilot AI](https://studypilot-ai-7fzx.onrender.com/)**
*(Note: If the link takes a few seconds to load, the server is waking up from its idle state).*

---

## 🛠 Cloud Infrastructure & Setup (Render)

For those who wish to fork this repository and deploy their own instance on Render, follow the configuration below:

### 1. Repository Structure
Ensure the backend and frontend are organized as follows to allow Render to serve the application correctly:
- `/backend`: Contains `app.py` and `requirements.txt`.
- `/frontend`: Contains all static UI assets (`index.html`, `style.css`, `script.js`).

### 2. Render Web Service Configuration
- **Runtime:** `Python`
- **Root Directory:** `backend` (or `.` depending on your GitHub root)
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

### 3. Environment Variables (Required)
The system requires specific environment variables to be configured in the Render Dashboard (**Settings > Environment**). **DO NOT** hardcode these in your source code for security reasons.

| Key | Description |
| :--- | :--- |
| `GEMINI_API_KEY` | Your Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/). |
| `SUPABASE_URL` | Your Supabase project URL (for database connectivity). |
| `SUPABASE_ANON_KEY` | Your Supabase anonymous API key. |

---

## 🤖 AI Declaration
In compliance with the **Project 2030: MyAI Future** hackathon rules:
- **Core AI Engine:** Google Gemini 2.5 Flash.
- **Code Assistance:** Parts of the boilerplate Flask structure and interactive quiz rendering logic were co-developed with AI assistance to ensure robust error handling and multimodal compatibility.
- **Human Oversight:** All educational prompts and system architectures were manually designed to align with pedagogical principles.