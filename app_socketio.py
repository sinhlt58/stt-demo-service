import os
import json
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from models.user_session_data import UserSesssionDataManager

from stt.viettel_client import ViettelSTTClient

app = Flask(__name__, static_folder="front-end-react/build")
cors = CORS(app, resources={"*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

ss_data_manager = UserSesssionDataManager()

viettel_stt_client = ViettelSTTClient()
@socketio.on("stt")
def handle_stt(audio_chunk_bytes):
    global viettel_stt_client
    print("requesting viettel stt ...")
    stt_text = viettel_stt_client.decode(audio_chunk_bytes)
    emit("stt", stt_text)


@socketio.on("join")
def on_join(data):
    user_id = request.sid
    username = data["username"]
    room = data["room"]
    join_room(room)
    ss_data = ss_data_manager.get(user_id)
    if ss_data is not None:
        ss_data.join_room(room, username)

    send(username + " has entered the room.", to=room)

@socketio.on("leave")
def on_leave(data):
    user_id = request.sid
    username = data["username"]
    room = data["room"]
    leave_room(room)
    ss_data = ss_data_manager.get(user_id)
    if ss_data is not None:
        ss_data.leave_room()

    send(username + " has left the room.", to=room)


@socketio.on("connect")
def handle_connect():
    user_id = request.sid # Just use the session as id for convenience
    ss_data_manager.create(user_id)


@socketio.on("disconnect")
def handle_disconnect():
    user_id = request.sid
    ss_data_manager.clean(user_id)


@app.errorhandler(404)
def not_found(error):
    print(error)
    return jsonify({
        "code": 404,
        "description": "Not found"
    })


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def fallback(path):
    if path != "" and os.path.exists(f"{app.static_folder}/{path}"):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    socketio.run(app, port=5000)
