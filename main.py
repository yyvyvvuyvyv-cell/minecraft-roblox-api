from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store data in memory
minecraft_data = {"players": {}, "chat": []}
roblox_data = {"players": {}, "chat": []}

# --------------------------
# Minecraft Endpoints
# --------------------------

@app.route("/MCstate", methods=["POST"])
def mc_state():
    """Minecraft sends its data (positions, messages, etc.)"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    players = data.get("players", [])
    for player in players:
        username = player.get("username")
        if username:
            minecraft_data["players"][username] = player
            messages = player.get("messages", [])
            if messages:
                minecraft_data["chat"].extend([{"user": username, "msg": msg} for msg in messages])
    
    return jsonify({"status": "ok"}), 200

@app.route("/MCreceive", methods=["GET"])
def mc_receive():
    """Minecraft fetches Roblox info (messages & users)"""
    return jsonify(roblox_data)

# --------------------------
# Roblox Endpoints
# --------------------------

@app.route("/RBLXState", methods=["POST"])
def rblx_state():
    """Roblox sends its messages"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    players = data.get("players", [])
    for player in players:
        username = player.get("username")
        if username:
            roblox_data["players"][username] = player
            messages = player.get("messages", [])
            if messages:
                roblox_data["chat"].extend([{"user": username, "msg": msg} for msg in messages])
    
    return jsonify({"status": "ok"}), 200

@app.route("/RBLXreceive", methods=["GET"])
def rblx_receive():
    """Roblox fetches Minecraft info (positions, messages, users)"""
    return jsonify(minecraft_data)

# --------------------------
# Run server
# --------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
