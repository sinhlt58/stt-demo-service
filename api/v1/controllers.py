from flask import Blueprint, jsonify, request
from flask import current_app as app

import logging
import json
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

api_v1 = Blueprint(
    "api_v1_blueprint",
    __name__,
    url_prefix="/api/v1",
)


@api_v1.route("/stt", methods=["POST"])
def detect_aa(path=None):
    json_body = request.json
    base64_audio = json_body.get("base64_audio")

    stt_service = app.config["stt_service"]
    text = stt_service.inferBase64(base64_audio)

    res = {
        "text": text
    }

    return jsonify(res)
