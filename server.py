from flask import Flask, request, jsonify

app = Flask(__name__)

AUTH_KEY = "9A68UHR237LtyUad901Hyae69YOYOWHATUP5042"

latest_command = {"code": "", "target": ""}

@app.route("/")
def home():
    return "Server is up and running!", 200

current_players = []

@app.route("/update_players", methods=["GET", "POST"])
def update_players():
    global current_players

    if request.method == "POST":
        data = request.get_json()
        if not data or data.get("key") != AUTH_KEY:
            return "Forbidden", 403
        current_players = data.get("players", [])
        return "✅ Updated", 200

    return jsonify(current_players or [])

@app.route("/command", methods=["POST"])
def command():
    global latest_command
    data = request.get_json()
    if not data or data.get("key") != "9A68UHR237LtyUad901Hyae69YOYOWHATUP5042":
        return "Unauthorized", 403
    code = data.get("code", "")
    target = data.get("target", "")
    if not code or not target:
        return "Missing code or target", 400
    latest_command = {"code": code, "target": target}
    return "✅ Command received."


@app.route("/fetch", methods=["GET"])
def fetch():
    global latest_command
    code = latest_command
    latest_command = ""  # Clear after fetch so it doesn't repeat forever
    return jsonify({"code": code})


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 1234))
    app.run(host="0.0.0.0", port=port)
