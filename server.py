from flask import Flask, request, jsonify

app = Flask(__name__)

latest_command = ""

@app.route("/")
def home():
    return "Server is up and running!", 200

current_players = []

@app.route("/update_players", methods=["GET", "POST"])
def update_players():
    global current_players

    if request.method == "POST":
        data = request.get_json()
        if not data or data.get("key") != "1234":
            return "Forbidden", 403
        current_players = data.get("players", [])
        return "✅ Updated", 200

    # This is for the GUI (GET)
    return jsonify(current_players or [])


@app.route("/command", methods=["POST"])
def command():
    global latest_command
    data = request.get_json()
    if not data or data.get("key") != "1234":  # Change "1234" to your secret key bro
        return "Unauthorized", 403
    code = data.get("code", "")
    latest_command = code
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
