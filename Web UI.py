import os

folder_path = r"D:\07-SANKET\Task\templates"
file_path = os.path.join(folder_path, "index.html")

# Create the folder
os.makedirs(folder_path, exist_ok=True)

# HTML content with Slack verification
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>HRHelper – Chatbot</title>
  <meta name="slack-app-verification" content="1" />
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to right, #e0eafc, #cfdef3);
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    .chat-container {
      background-color: white;
      width: 100%;
      max-width: 500px;
      box-shadow: 0 8px 16px rgba(0,0,0,0.2);
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .chat-header {
      background-color: #007bff;
      color: white;
      padding: 15px;
      text-align: center;
      font-size: 20px;
      font-weight: bold;
    }

    #chat-box {
      padding: 15px;
      height: 400px;
      overflow-y: auto;
      background-color: #f9f9f9;
      flex-grow: 1;
    }

    .chat-entry {
      margin-bottom: 10px;
    }

    .chat-entry strong {
      display: block;
      margin-bottom: 3px;
      color: #333;
    }

    .chat-entry p {
      margin: 0;
      padding: 8px 12px;
      background-color: #e6e6e6;
      border-radius: 8px;
      display: inline-block;
      max-width: 80%;
    }

    .user p {
      background-color: #007bff;
      color: white;
      align-self: flex-end;
    }

    .input-area {
      display: flex;
      border-top: 1px solid #ccc;
    }

    #user-input {
      flex-grow: 1;
      padding: 10px;
      border: none;
      font-size: 16px;
      border-radius: 0;
    }

    button {
      padding: 10px 15px;
      background-color: #007bff;
      color: white;
      border: none;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>
  <div class="chat-container">
    <div class="chat-header">💬  HR Helper – Employee FAQ Chatbot</div>
    <div id="chat-box"></div>
    <div class="input-area">
      <input type="text" id="user-input" placeholder="Ask your HR question..." />
      <button onclick="sendMessage()">Send</button>
    </div>
  </div>

  <script>
  async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="chat-entry user"><strong>You:</strong><p>${message}</p></div>`;

    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      chatBox.innerHTML += `<div class="chat-entry bot"><strong>Bot:</strong><p>${data.answer}</p></div>`;
      chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
      chatBox.innerHTML += `<div class="chat-entry bot"><strong>Bot:</strong><p>Error getting response.</p></div>`;
    }
  }

  // Trigger sendMessage() on Enter key press inside the input box
  document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault();
      sendMessage();
    }
  });
  </script>
</body>
</html>
'''

with open(file_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f" index.html created successfully at {file_path}")
