from flask import Flask, Response, render_template, request, redirect
import cv2
from utils.constants import *
from postgres.postgres import *
from User.CRUD import *
from utils.FaceRandCameraVariable import restart_CF_DICT_VARIABLES
from utils.GlobalVariables import *
from faceRecogination.utils import *
from flaskwebgui import FlaskUI
import ctypes
import time
import base64
from flask import jsonify

app = Flask(__name__)


def gen():
    global Camera_variables
    start_time = time.time()
    while time.time()-start_time <= 5:
        if len(Camera_variables['frame']) == 0:
            continue
        time.sleep(0.04)
        start_time = time.time()
        _, buffer = cv2.imencode('.png', Camera_variables['frame'])
        frame_byte = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_byte + b'\r\n\r\n')


@app.route('/get_capture', methods=['GET'])
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_face_and_encodings', methods=['GET'])
def getFaceAndEncodings():
    start_time = time.time()
    while time.time()-start_time <= 5:
        face_locations, face_encodings = get_face_locations_and_encodings()
        if len(face_locations) != 0:
            top, right, bottom, left = face_locations[0]
            top *= SCALE_PERCENT
            right *= SCALE_PERCENT
            bottom *= SCALE_PERCENT
            left *= SCALE_PERCENT
            crop_img = Camera_variables['frame'][top:bottom, left:right]
            _, buffer = cv2.imencode('.jpg', crop_img)
            jpg_as_str = "data:image/jpg;base64," + \
                base64.b64encode(buffer).decode("utf-8")
            return jsonify({'img': jpg_as_str, 'face_encodings': list(face_encodings[0])})
    return 'Yuz Topilmadi yoki Kamera Ishlamayapti!!', 400


@app.route('/createworker', methods=['GET'])
def createworkerGET():
    return render_template('createWorker.html')


@app.route('/createworker', methods=['POST'])
def createworkerPOST():
    alert_message = validate_and_create_worker(request.form.to_dict())
    if alert_message is not None:
        return render_template('createWorker.html', **alert_message)
    return redirect('workers')


@app.route('/updateworker', methods=['POST'])
def updateworkerPOST():
    alert_message = validate_and_update_worker(request.form.to_dict())
    if alert_message is not None:
        return render_template('updateWorker.html', **alert_message)
    return redirect('workers')


@app.route('/updateworker', methods=['GET'])
def updateworkerGET():
    if request.args.get("id") is not None:
        worker_id = int(request.args.get("id"))
        if worker_id in workers.index:
            user = workers.loc[worker_id]
            return render_template('updateWorker.html', **user.to_dict(), id=worker_id)
    return render_template('404.html')


@app.route('/', methods=['GET'])
def home():
    return redirect('workers')


@app.route('/workers', methods=['GET'])
def get_workers():
    return render_template('workers.html', workers=workers.to_dict(orient='index'))


@app.route('/inoutcome', methods=['GET'])
def inoutcome():
    return render_template('inoutcome.html')


@app.route('/storage', methods=['GET'])
def storage():
    return render_template('storage.html')


@app.route('/set_camera_url', methods=['POST'])
def set_camera_url():
    camera_url = request.form.get('camera_url')
    if camera_url is not None and camera_url != '':
        set_camera_url_file(camera_url)
        restart_CF_DICT_VARIABLES()
    return redirect('capture')


@app.route('/analytics', methods=['GET','POST'])
def get_analytics():
    analytics = validate_and_get_analytics(request.form.to_dict())
    return render_template('analytics.html', **analytics)


@app.route('/capture', methods=['GET'])
def capture():
    return render_template('capture.html', camera_url=str(Camera_variables['CAMERA_URL']))


@app.route('/capturefull', methods=['GET'])
def capturefull():
    return render_template('captureFull.html')


@app.route('/workers_is_come', methods=['POST'])
def workers_is_come_post():
    add_attendance(request.form.to_dict())
    return redirect('workers_is_come')


@app.route('/workers_is_come', methods=['GET'])
def workers_is_come():
    data = validate_and_get_workers_is_come(request.form.to_dict())
    return render_template('workersIsCome.html', **data,
                           workers=workers.reset_index().to_dict(orient='records'))


@app.route('/deleteworker/<id>', methods=['GET'])
def deleteworker(id):
    delete_worker_db(id)
    if int(id) in workers.index:
        workers.drop(int(id), inplace=True)
    return get_workers()


@app.route('/deleteattendance/<id>', methods=['GET'])
def deleteattendance(id):
    delete_attendance_db(id)
    return workers_is_come()


if __name__ == '__main__':
    # Prod
    restart_CF_DICT_VARIABLES()
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    FlaskUI(app=app, server="flask", port=51232).run()
