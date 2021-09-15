import os
import json
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__, static_folder="front-end-react/build")
cors = CORS(app, resources={"*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on("stt")
def handle_stt(audio_chunk_bytes):
    # print(type(audio_chunk_bytes))

    emit("stt", "stt text " + str(random.randint(0, 10000000)))


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


@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def fallback(path):
    if path != "" and os.path.exists(f"{app.static_folder}/{path}"):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    socketio.run(app)
