let lastTopic = "";
let lastQuizText = "";

function askAI(forceMode = null) {
  const topicInput = document.getElementById("topic").value;
  const mode = forceMode || document.getElementById("mode").value;
  const output = document.getElementById("output");
  const actions = document.getElementById("actions");

  if (topicInput) {
    lastTopic = topicInput;
  }

  if (!lastTopic) {
    alert("Please enter a topic first.");
    return;
  }

  output.innerText = "AI is processing...";
  actions.classList.add("hidden");

  const payload = {
    topic: lastTopic,
    mode: mode,
    quizText: lastQuizText
  };

  fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(res => res.json())
    .then(data => {
      if (mode === "quiz") {
        lastQuizText = data.result;
        renderQuiz(data.result);
      } else {
        output.innerText = data.result || "";
      }
      actions.classList.remove("hidden");
    });
}

/**
 * Render quiz questions with radio buttons.
 * This parser is intentionally tolerant because
 * LLM output format is not guaranteed.
 */
function renderQuiz(text) {
  const output = document.getElementById("output");
  output.innerHTML = "";

  if (!text) {
    output.innerText = "No quiz generated.";
    return;
  }

  const lines = text.split("\n");
  let qIndex = 0;

  lines.forEach(line => {
    const cleanLine = line.trim();

    // ✅ Question line: starts with number
    if (/^\d+[\.\)]?/.test(cleanLine)) {
      qIndex++;
      output.innerHTML += `<p><strong>${cleanLine}</strong></p>`;
      return;
    }

    // ✅ Option line: A / B / C / D with flexible separators
    if (/^[A-D][\.\):\- ]/.test(cleanLine)) {
      const optionLetter = cleanLine.charAt(0);
      const optionText = cleanLine.substring(1).trim();

      output.innerHTML += `
        <label style="display:block; margin-left:20px;">
          <input type="radio" name="q${qIndex}">
          <strong>${optionLetter}</strong>${optionText}
        </label>
      `;
      return;
    }
  });
}

function nextAction(mode) {
  askAI(mode);
}
