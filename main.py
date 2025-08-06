from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
chat_log = []

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Roblox Chat Logger</title>
    <style>
        body {
            background-color: #1d1d1d;
            color: white;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        #chat-container {
            max-width: 800px;
            margin: auto;
            padding: 2rem;
        }
        h1 {
            text-align: center;
            color: #00b2ff;
        }
        #chat-log {
            background: #2b2b2b;
            padding: 1rem;
            border-radius: 10px;
            height: 500px;
            overflow-y: scroll;
        }
        .chat-line {
            margin-bottom: 0.5rem;
        }
        .time {
            color: #aaaaaa;
            margin-right: 0.5rem;
        }
        .username {
            color: #00ffb2;
            font-weight: bold;
            margin-right: 0.3rem;
        }
        .message {
            color: white;
        }
    </style>
    <script>
        async function fetchMessages() {
            const res = await fetch("/messages");
            const data = await res.json();
            const log = document.getElementById("chat-log");
            log.innerHTML = "";
            data.forEach(msg => {
                const line = document.createElement("div");
                line.className = "chat-line";
                line.innerHTML = `<span class="time">[${msg.time}]</span> <span class="username">${msg.username}:</span> <span class="message">${msg.message}</span>`;
                log.appendChild(line);
            });
        }
        setInterval(fetchMessages, 1000);
        window.onload = fetchMessages;
    </script>
</head>
<body>
    <div id="chat-container">
        <h1>Live Roblox Chat</h1>
        <div id="chat-log"></div>
    </div>
</body>
</html>
'''

@app.route("/")
def index():
    return HTML_TEMPLATE

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data"}), 400

    username = data.get("username", "Unknown")
    message = data.get("message", "")
    timestamp = datetime.fromtimestamp(data.get("time", datetime.now().timestamp())).strftime("%H:%M:%S")

    chat_log.append({"username": username, "message": message, "time": timestamp})
    if len(chat_log) > 100:
        chat_log.pop(0)
    return jsonify({"status": "ok"}), 200

@app.route("/messages")
def get_messages():
    return jsonify(chat_log)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
