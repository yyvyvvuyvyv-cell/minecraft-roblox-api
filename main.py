from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

minecraft_data = {"players": {}, "chat": []}
roblox_data = {"players": {}, "chat": []}

# --------------------------
# Minecraft Endpoints
# --------------------------

@app.route("/MCstate", methods=["POST", "GET"])
def mc_state():
    if request.method == "POST":
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
    else:  # GET
        return jsonify(minecraft_data)

@app.route("/MCreceive", methods=["POST", "GET"])
def mc_receive():
    if request.method == "POST":
        data = request.get_json()
        # optional: handle updates from Roblox if needed
        return jsonify({"status": "ok"}), 200
    return jsonify(roblox_data)

# --------------------------
# Roblox Endpoints
# --------------------------

@app.route("/RBLXState", methods=["POST", "GET"])
def rblx_state():
    if request.method == "POST":
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
    else:  # GET
        return jsonify(roblox_data)

@app.route("/RBLXreceive", methods=["POST", "GET"])
def rblx_receive():
    if request.method == "POST":
        data = request.get_json()
        # optional: handle updates from Minecraft if needed
        return jsonify({"status": "ok"}), 200
    return jsonify(minecraft_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
