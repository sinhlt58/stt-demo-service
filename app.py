import os
import logging
import json
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from stt.stt_client import STTClient
from api.v1.controllers import api_v1

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__, static_folder="front-end-react/build")
    cors = CORS(app, resources={"*": {"origins": "*"}})

    # Configurations
    try:
        env = os.environ["FLASK_ENV"]
    except KeyError:
        env = "production"
    logger.info("env: {}".format(env))
    app.config.from_object("config.%s" % str(env).capitalize())

    # setup global objects
    app.config["stt_service"] = STTClient()

    # socketio
    # app.config["socketio"] = SocketIO(app)

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

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    app.register_blueprint(api_v1)

    return app
