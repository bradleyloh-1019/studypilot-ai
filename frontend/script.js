function askAI() {
  const topic = document.getElementById("topic").value;
  const mode = document.getElementById("mode").value;

  if (!topic) {
    alert("Please enter a topic");
    return;
  }

  fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      topic: topic,
      mode: mode
    })
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("output").innerText = data.result;
  })
  .catch(error => {
    document.getElementById("output").innerText = "Error connecting to AI backend.";
    console.error(error);
  });
}
