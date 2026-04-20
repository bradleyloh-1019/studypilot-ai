let lastTopic = "";
let lastQuizText = "";
let currentImageBase64 = null; 
let currentImageMimeType = null; 

// 监听图片上传并转换为 Base64
document.addEventListener('DOMContentLoaded', () => {
  const imageInput = document.getElementById('imageInput');
  if(imageInput) {
    imageInput.addEventListener('change', function(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
          // 提取纯 Base64 数据
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

function askAI(forceMode = null) {
  const topicInput = document.getElementById("topic").value;
  const mode = forceMode || document.getElementById("mode").value;
  const output = document.getElementById("output");
  const actions = document.getElementById("actions");

  if (topicInput) {
    lastTopic = topicInput;
  }

  // 验证：必须输入文字或者上传了图片
  if (!lastTopic && !currentImageBase64) {
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
    image_mime_type: currentImageMimeType 
  };

  fetch("/ask", {
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

  lines.forEach(line => {
    const cleanLine = line.trim();
    if (!cleanLine) return;

    const testLine = cleanLine.replace(/\*\*/g, "").replace(/^[\*\-]\s+/, "").trim();

    if (/^\d+[\.\)]/.test(testLine)) {
      qIndex++;
      output.innerHTML += `<div style="margin-top: 20px; margin-bottom: 10px;"><strong>${testLine}</strong></div>`;
      return;
    }

    if (/^[A-D][\.\):\- ]/.test(testLine)) {
      const match = testLine.match(/^([A-D])[\.\):\- ]+(.*)/);
      if (match) {
        const optionLetter = match[1];
        const optionText = match[2];
        
        output.innerHTML += `
          <label>
            <input type="radio" name="q${qIndex}">
            <strong>${optionLetter}.</strong> ${optionText}
          </label>
        `;
      }
      return;
    }

    output.innerHTML += `<p>${testLine}</p>`;
  });
}

function nextAction(mode) {
  askAI(mode);
}