let lastTopic = "";
let lastQuizText = "";
let currentImageBase64 = null; 
let currentImageMimeType = null; 

document.addEventListener('DOMContentLoaded', () => {
  const imageInput = document.getElementById('imageInput');
  if(imageInput) {
    imageInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
          currentImageBase64 = event.target.result.split(',')[1];
          currentImageMimeType = file.type;
        };
        reader.readAsDataURL(file);
      } else {
        currentImageBase64 = null;
        currentImageMimeType = null;
      }
    });
  }
});

function askAI(forceMode = null, extraData = null) {
  const topicInput = document.getElementById("topic").value;
  const mode = forceMode || document.getElementById("mode").value;
  const output = document.getElementById("output");
  const actions = document.getElementById("actions");

  if (topicInput) {
    lastTopic = topicInput;
  }

  if (!lastTopic && !currentImageBase64 && mode !== 'grade') {
    alert("Please enter a topic or upload an image first.");
    return;
  }

  output.innerHTML = "<p style='color: #6b7280;'>AI is thinking... please wait 🚀</p>";
  actions.classList.add("hidden");

  const payload = {
    topic: lastTopic,
    mode: mode,
    quizText: lastQuizText,
    image_data: currentImageBase64,       
    image_mime_type: currentImageMimeType,
    user_answers: extraData
  };

  fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  })
    .then(async res => {
      if (!res.ok) {
        throw new Error(`Server returned status ${res.status}. Please check backend logs.`);
      }
      return res.json();
    })
    .then(data => {
      if (mode === "quiz") {
        lastQuizText = data.result;
        renderQuiz(data.result);
      } else {
        output.innerHTML = marked.parse(data.result || "No response generated.");
      }
      actions.classList.remove("hidden");
    })
    .catch(err => {
      output.innerHTML = `<p style="color: red;">Connection error: ${err.message}</p>`;
      actions.classList.remove("hidden");
    });
}

function renderQuiz(text) {
  const output = document.getElementById("output");
  output.innerHTML = "";

  if (!text) {
    output.innerText = "No quiz generated.";
    return;
  }

  const lines = text.split("\n");
  let qIndex = 0;
  let htmlContent = "";

  lines.forEach(line => {
    const cleanLine = line.trim();
    if (!cleanLine) return;

    const testLine = cleanLine.replace(/\*\*/g, "").replace(/^[\*\-]\s+/, "").trim();

    if (/^\d+[\.\)]/.test(testLine)) {
      qIndex++;
      htmlContent += `<div style="margin-top: 20px; margin-bottom: 10px;"><strong>${testLine}</strong></div>`;
      return;
    }

    if (/^[A-D][\.\):\- ]/.test(testLine)) {
      const match = testLine.match(/^([A-D])[\.\):\- ]+(.*)/);
      if (match) {
        const optionLetter = match[1];
        const optionText = match[2];
        
        htmlContent += `
          <label>
            <input type="radio" name="q${qIndex}" value="${optionLetter}">
            <strong>${optionLetter}.</strong> ${optionText}
          </label>
        `;
      }
      return;
    }

    htmlContent += `<p>${testLine}</p>`;
  });

  if (qIndex > 0) {
    htmlContent += `
      <div style="margin-top: 24px; text-align: center;">
        <button onclick="submitQuiz(${qIndex})" style="background: #10b981; max-width: 250px;">Submit & Grade Quiz</button>
      </div>
    `;
  }

  output.innerHTML = htmlContent;
}

function submitQuiz(totalQuestions) {
  let userAnswers = [];
  let allAnswered = true;

  for (let i = 1; i <= totalQuestions; i++) {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    if (selected) {
      userAnswers.push(`Q${i}: ${selected.value}`);
    } else {
      userAnswers.push(`Q${i}: Skipped`);
      allAnswered = false;
    }
  }

  if (!allAnswered) {
    if (!confirm("You haven't answered all questions. Are you sure you want to submit?")) {
      return;
    }
  }

  const answersString = userAnswers.join(", ");
  askAI('grade', answersString);
}

function nextAction(mode) {
  askAI(mode);
}