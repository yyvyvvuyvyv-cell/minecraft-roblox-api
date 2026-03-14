from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

state = {
    "players": {},
    "chat": [],
    "server": {}
}

@app.route("/state", methods=["POST"])
def update_state():
    data = request.get_json()

    if "players" in data:
        for p in data["players"]:
            state["players"][p["name"]] = p

    if "chat" in data:
        state["chat"].extend(data["chat"])

    if "server" in data:
        state["server"] = data["server"]

    return jsonify({"status":"ok"})


@app.route("/state", methods=["GET"])
def get_state():
    global state

    response = state.copy()
    response["chat"] = state["chat"]

    state["chat"] = []  # clear chat after sending

    return jsonify(response)


app.run(host="0.0.0.0", port=10000)
