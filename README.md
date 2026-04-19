## Getting Started

This project requires Python and a locally running Ollama LLM.

To run the project:
1. Start the Flask backend
2. Open the frontend in a web browser

# StudyPilot AI
Your Smart AI Learning Assistant


![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/backend-flask-black)
![AI](https://img.shields.io/badge/AI-Gemma%20LLM-green)


---

## 📘 Project Overview

StudyPilot AI is an AI-powered learning assistant designed to support students in understanding academic concepts, assessing their knowledge, and improving exam preparation across multiple subjects.

Instead of functioning as a simple question–answer chatbot, StudyPilot AI guides learners through a structured learning workflow that includes concept explanation, self-testing, delayed feedback, and targeted study advice. The system is intentionally designed to reflect real educational and revision practices rather than instant-answer interactions.

---

## 🎯 Target Users & Learning Assumption

StudyPilot AI is designed with a clear learner assumption:

**The system assumes the user is a student preparing for assessments or examinations at secondary, pre-university, or diploma level.**

This learner assumption is embedded directly into the backend AI prompt design and affects:
- The tone and depth of explanations
- The difficulty and structure of quiz questions
- The timing of feedback delivery
- The nature of study advice provided

All responses prioritise exam-relevant understanding rather than casual discussion.

---

## ❓ Problem Statement

Many students struggle with:
- Understanding abstract academic concepts
- Identifying gaps in their own knowledge
- Practicing effective self-assessment
- Receiving useful feedback after quizzes
- Structuring efficient revision strategies

Most existing AI tools provide instant answers but fail to support a complete learning cycle. StudyPilot AI addresses this gap by integrating AI into a structured educational workflow that encourages active learning and reflection.

---

## ✅ Core Features

### 1. Explain Concept (AI as Tutor)
- Explains academic topics across multiple subjects
- Tailors explanations for exam-oriented learning
- Responds using the same language as the user’s input

---

### 2. Generate Quiz (AI as Assessor)
- Generates multiple-choice questions for self-assessment
- Focuses on testing conceptual understanding
- Answers are intentionally hidden to encourage user attempt
- Variation logic reduces repetitive quiz generation

---

### 3. Reveal Answers (Delayed Feedback)
- Answers are revealed only after a quiz is generated
- Provides correct answers with concise explanations
- Encourages active recall before feedback

---

### 4. Study Tips (AI as Study Coach)
- Identifies key concepts to revise
- Highlights common exam-related mistakes
- Suggests practical and effective revision strategies

---

## 🧠 Educational Design Principles

StudyPilot AI is designed around established learning principles:

### Active Recall
Learners attempt quiz questions before seeing correct answers.

### Delayed Feedback
Separating quiz attempts from answer explanations improves retention.

### Learning Stage Awareness
The AI dynamically switches roles depending on learning stage:
- Tutor for explanation
- Assessor for testing
- Study Coach for revision guidance

---

## 🏗 System Architecture

StudyPilot AI follows a client–server architecture with a locally hosted AI model.

### High-Level Architecture Overview

StudyPilot AI adopts a client–server architecture where all AI processing is handled locally.  
The system is designed to ensure that AI logic is central to the learning workflow while keeping the overall structure simple, secure, and easy to understand.

At a high level, the system consists of four main layers:

- User Interface (Frontend)
- Application Logic (Backend)
- AI Runtime
- Large Language Model

The overall execution flow is as follows:

1. The user enters a topic and selects a learning action (Explain, Quiz, or Study Tips) from the frontend interface.
2. The frontend sends the user request to the backend using an HTTP POST request in JSON format.
3. The Flask backend receives the request and validates the input.
4. Based on the selected action, the backend determines the current learning stage and assigns an appropriate AI role (Tutor, Assessor, or Study Coach).
5. A role-specific prompt is constructed, incorporating the learner assumption that the user is preparing for assessments or examinations.
6. The prompt is sent to the Ollama runtime for local AI processing.
7. The Gemma Large Language Model performs inference and generates the requested output.
8. The AI-generated result is returned to the backend.
9. The backend forwards the response to the frontend.
10. The frontend displays the output to the user, allowing further interaction or progression to the next learning stage.

---

### Architecture Diagram

```mermaid
graph TD
    U[User]
    F[Frontend UI<br/>HTML / CSS / JavaScript]
    B[Backend API<br/>Flask app.py]
    O[Ollama Runtime<br/>Local AI Server]
    L[Gemma LLM<br/>Local Model]

    U --> F
    F -->|HTTP POST (JSON)| B
    B -->|Prompt Request| O
    O -->|Model Inference| L
    L -->|Generated Output| O
    O --> B
    B --> F

    This diagram represents a closed-loop system in which all AI processing is performed locally. The frontend manages user interaction, the backend enforces learning logic, and the AI runtime handles content generation.

Component-Level Architecture
Frontend (HTML / CSS / JavaScript)
The frontend is responsible for user interaction and presentation. Its key responsibilities include:

Capturing user input such as topic selection and learning mode
Displaying AI-generated explanations, quizzes, and study tips
Rendering multiple-choice quiz questions with selectable options
Providing navigation between learning stages

The frontend does not contain any AI logic, ensuring a clean separation of concerns.

Backend API (Flask – app.py)
The Flask backend serves as the core control layer of the system. It is responsible for:

Receiving and validating requests from the frontend
Enforcing the learning workflow (Explain → Quiz → Reveal → Study)
Managing temporary state such as the current topic and quiz context
Constructing role-based prompts for the AI
Preventing invalid actions (e.g. revealing answers without a quiz)

By centralising logic in the backend, consistency in learning behaviour is maintained.

Ollama Runtime
Ollama functions as the local AI runtime responsible for executing AI prompts. It receives prompt instructions from the backend and handles inference locally without requiring internet access or external API keys.

Gemma Large Language Model
Gemma is the Large Language Model used by StudyPilot AI. It is responsible for:

Generating concept explanations
Creating assessment-style quiz questions
Producing delayed feedback for answer revelation
Providing study tips and revision strategies

The model operates entirely on the local machine, ensuring privacy and security.

Detailed Execution Flow
The system executes requests in the following sequence:

The user selects a topic and a learning action from the frontend.
The frontend sends the request to the backend as a JSON payload.
The backend validates the request and determines the learning stage.
A role-specific prompt is constructed based on the learner assumption.
The prompt is sent to the Ollama runtime for processing.
The Gemma model generates the requested content.
Ollama returns the result to the backend.
The backend returns the processed response to the frontend.
The frontend renders the output and enables the next appropriate learning action.

This structured data flow ensures that AI behaviour is consistent, educationally intentional, and tightly integrated into the learning process.

---
