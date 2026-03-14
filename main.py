from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

player_positions = {}
chat_messages = []
roblox_chat_queue = []


@app.route("/positions", methods=["POST"])
def update_positions():
    data = request.get_json()

    for player in data.get("players", []):
        username = player.get("username")

        player_positions[username] = {
            "x": player.get("x"),
            "y": player.get("y"),
            "z": player.get("z"),
            "yaw": player.get("yaw"),
            "pitch": player.get("pitch")
        }

    return jsonify({"status": "ok"})


@app.route("/chat", methods=["POST"])
def minecraft_chat():
    data = request.get_json()

    chat_messages.append({
        "username": data.get("username"),
        "message": data.get("message")
    })

    return jsonify({"status": "ok"})


@app.route("/robloxchat", methods=["POST"])
def roblox_chat():
    data = request.get_json()

    roblox_chat_queue.append({
        "username": data.get("username"),
        "message": data.get("message")
    })

    return jsonify({"status": "ok"})


@app.route("/robloxchat", methods=["GET"])
def get_roblox_chat():
    global roblox_chat_queue

    messages = roblox_chat_queue
    roblox_chat_queue = []

    return jsonify(messages)


@app.route("/state", methods=["GET"])
def get_state():
    global chat_messages

    messages = chat_messages
    chat_messages = []

    return jsonify({
        "players": player_positions,
        "chat": messages
    })


@app.route("/")
def home():
    return "Minecraft ↔ Roblox API Running"


app.run(host="0.0.0.0", port=10000)
