from flask import Flask, request, send_file, Response, render_template
import time
import socket
import os
import io
import cv2

dir_path = os.path.dirname(os.path.realpath(__file__))
tmp_img_path = os.path.join(
    dir_path, 'remote', 'python server', 'tmp_photo', 'tmp_img.jpg')

app = Flask(__name__)
vc = cv2.VideoCapture(0)

@app.route("/move")
def move():
    forward = bool(request.args.get('forward'))
    cm = float(request.args.get('cm'))
    return "Moved."

def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        frame = cv2.flip(frame, flipCode=-1)
        cv2.imwrite(tmp_img_path, frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open(tmp_img_path, 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=80)