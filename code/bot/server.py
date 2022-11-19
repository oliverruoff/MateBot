from flask import Flask, request, Response
import cv2


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
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=5000)