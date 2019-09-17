from flask import Flask, request, redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException
import json
import uuid
import recognition
import os
import base64
import traceback

app = Flask(__name__)

APP_VERSION = "0.0.1"
SWAGGER_URL = '/api/v1/docs'
API_URL = '/api/v1/swagger.json'


@app.route('/api/v1/face-locations', methods=['POST'])
def face_locations():
    file_path = "uploads/" + str(uuid.uuid4()) + ".jpg"

    f = request.files['image']
    f.save(file_path)

    out = recognition.face_locations(file_path)
    os.remove(file_path)

    if len(out['face_landmarks_list']) == 0:
        return json.dumps({
            "message": "No face found"
        }), 422

    out_w_lands_base64 = base64.b64encode(out['image_with_landmarks'].getvalue()).decode('ascii')
    face = {
        "app_version": APP_VERSION,
        "face_landmarks_list": out['face_landmarks_list'],
        "image_with_landmarks": "data:image/jpg;base64," + out_w_lands_base64
    }

    return json.dumps(face), 200


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": traceback.format_exc()
    })
    return response


@app.route('/', methods=['POST', 'GET'])
def main_route():
    return redirect(SWAGGER_URL, code=302)


@app.route(API_URL, methods=['GET'])
def swagger_json():
    # edit scheme: https://editor.swagger.io/
    return send_from_directory('docs', 'swagger.json')


swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "image_face_detector"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
