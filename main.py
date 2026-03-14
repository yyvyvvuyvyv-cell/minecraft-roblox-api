# main.py
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
    
    # Handle plain list from Minecraft plugin
    if isinstance(data, list):
        for player in data:
            username = player.get("name")  # use "name" from Minecraft plugin
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

    # Optional: handle {"players": [...]} format too
    elif isinstance(data, dict) and "players" in data:
        for player in data["players"]:
            username = player.get("username") or player.get("name")
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

    return jsonify({"error": "Invalid format"}), 400

@app.route("/positions", methods=["GET"])
def get_positions():
    return jsonify({"players": player_positions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
