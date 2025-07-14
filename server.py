from flask import Flask, request, jsonify

app = Flask(__name__)

latest_command = {}

current_players = []

AUTH_KEY = "9A68UHR237LtyUad901Hyae69YOYOWHATUP5042"

@app.route("/")
def home():
    return "Server is up and running!", 200

@app.route("/update_players", methods=["GET", "POST"])
def update_players():
    global current_players

    if request.method == "POST":
        data = request.get_json()
        if not data or data.get("key") != AUTH_KEY:
            return "Forbidden", 403
        current_players = data.get("players", [])
        return "✅ Updated", 200

    # GET for GUI
    return jsonify(current_players or [])

@app.route("/command", methods=["POST"])
def command():
    global latest_command
    data = request.get_json()
    if not data or data.get("key") != AUTH_KEY:
        return "Unauthorized", 403

    # Expect "command", "args", "target"
    command = data.get("command", "")
    args = data.get("args", "")
    target = data.get("target", "")

    if not command or not target:
        return "Invalid payload", 400

    latest_command = {
        "command": command,
        "args": args,
        "target": target
    }
    return "✅ Command received."

@app.route("/fetch", methods=["GET"])
def fetch():
    global latest_command
    cmd = latest_command
    latest_command = {}  # Clear after fetch
    return jsonify(cmd)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 1234))
    app.run(host="0.0.0.0", port=port)
