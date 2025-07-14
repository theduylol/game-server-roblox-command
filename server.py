from flask import Flask, request, jsonify

app = Flask(__name__)
latest_command = ""

@app.route("/command", methods=["POST"])
def command():
    global latest_command
    data = request.get_json()
    if data.get("key") != "1234":
        return "Unauthorized", 403
    latest_command = data["code"]
    return "✅ Command received."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1234)
