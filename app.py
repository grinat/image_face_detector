from flask import Flask, request, redirect, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException
import json
import recognition, file_operations
import base64
import traceback

app = Flask(__name__)
CORS(app)

APP_VERSION = "0.0.3"
SWAGGER_URL = '/api/v1/docs'
API_URL = '/api/v1/swagger.json'
OUT_IMAGE_SZ = 512


@app.route('/api/v1/face-landmarks', methods=['POST'])
def face_landmarks():
    file_path = file_operations.save_file_and_return_path(request)

    out_image_sz = OUT_IMAGE_SZ
    if 'out_image_sz' in request.form and int(request.form['out_image_sz']) > 0:
        out_image_sz = int(request.form['out_image_sz'])

    # detect face landmarks
    out = recognition.face_landmarks(file_path, out_image_sz)

    # remove file after recognize
    file_operations.remove_file(file_path)

    if len(out['face_landmarks_list']) == 0:
        return json.dumps({
            "code": "image_no_face",
            "message": "No face found"
        }), 422

    # all images we return in base64 for fast use in browser
    out_w_lands_base64 = base64.b64encode(out['image_with_landmarks'].getvalue()).decode('ascii')

    result = {
        "app_version": APP_VERSION,
        # coords returning for original image
        "face_landmarks_list": out['face_landmarks_list'],
        "face_count": len(out['face_landmarks_list']),
        "image": "data:image/jpg;base64," + out_w_lands_base64,
    }

    return json.dumps(result), 200


@app.route('/api/v1/face-locations', methods=['POST'])
def face_locations():
    file_path = file_operations.save_file_and_return_path(request)

    out_image_sz = OUT_IMAGE_SZ
    if 'out_image_sz' in request.form and int(request.form['out_image_sz']) > 0:
        out_image_sz = int(request.form['out_image_sz'])

    # detect faces
    out = recognition.face_locations(file_path, out_image_sz)

    # remove file after recognize
    file_operations.remove_file(file_path)

    if len(out['face_locations_list']) == 0:
        return json.dumps({
            "code": "image_no_face",
            "message": "No face found"
        }), 422

    faces_base64 = []
    for image in out['images']:
        faces_base64.append("data:image/jpg;base64," + base64.b64encode(image.getvalue()).decode('ascii'))

    # change pos, in format for PIL.ImageDraw.Draw.rectangle([x0, y0, x1, y1])
    pillow_rectangles = []
    for face_location in out['face_locations_list']:
        bottom, right, top, left = face_location
        pillow_rectangles.append((left, bottom, right, top))

    result = {
        "app_version": APP_VERSION,
        "face_locations": pillow_rectangles,
        "face_count": len(out['face_locations_list']),
        "images": faces_base64
    }

    return json.dumps(result), 200


@app.route('/api/v1/face-encodings', methods=['POST'])
def face_encodings():
    file_path = file_operations.save_file_and_return_path(request)

    out = recognition.face_encodings(file_path)

    # remove file after recognize
    file_operations.remove_file(file_path)

    if len(out['face_encodings_list']) == 0:
        return json.dumps({
            "code": "image_no_face",
            "message": "No face found"
        }), 422

    result = {
        "app_version": APP_VERSION,
        "face_encodings_list": out['face_encodings_list'],
        "face_count": len(out['face_encodings_list'])
    }

    return json.dumps(result), 200


@app.route('/api/v1/compare-faces', methods=['POST'])
def compare_faces():
    body = request.json

    haystack = body['haystack']
    needle = body['needle']
    tolerance = 0.6

    out = recognition.compare(haystack, needle)

    result = {
        "app_version": APP_VERSION,
        "face_distances": out['face_distances'],
        "faces": [dist <= tolerance for dist in out['face_distances']]
    }

    return json.dumps(result), 200


@app.route('/api/v1/face-metrics', methods=['POST'])
def face_metrics():
    file_path = file_operations.save_file_and_return_path(request)

    out = recognition.face_metrics(file_path)

    return json.dumps({
        "app_version": APP_VERSION,
        'face_landmarks_list': out['face_landmarks_list'],
        'face_encodings_list': out['face_encodings_list'],
        'face_locations_list': out['face_locations_list']
    }), 200


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
