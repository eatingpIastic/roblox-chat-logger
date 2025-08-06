from flask import Flask, request, render_template, jsonify
from datetime import datetime

app = Flask(__name__)
chat_log = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", messages=chat_log)

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    if not data: return jsonify({"error": "No data"}), 400

    username = data.get("username", "Unknown")
    message = data.get("message", "")
    timestamp = datetime.fromtimestamp(data.get("time", datetime.now().timestamp())).strftime("%H:%M:%S")

    chat_log.append({"username": username, "message": message, "time": timestamp})
    if len(chat_log) > 100: chat_log.pop(0)
    return jsonify({"status": "ok"}), 200

@app.route("/messages")
def get_messages():
    return jsonify(chat_log)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
