# File: main.py
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow Roblox to fetch data

# Store positions in memory
player_positions = {}

@app.route("/positions", methods=["POST"])
def update_positions():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    for player in data.get("players", []):
        username = player.get("username")
        x = player.get("x")
        y = player.get("y")
        z = player.get("z")
        yaw = player.get("yaw", 0)
        pitch = player.get("pitch", 0)
        if username:
            player_positions[username] = {
                "x": x, "y": y, "z": z, "yaw": yaw, "pitch": pitch
            }
    return jsonify({"status": "ok"}), 200

@app.route("/positions", methods=["GET"])
def get_positions():
    return jsonify({"players": player_positions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)