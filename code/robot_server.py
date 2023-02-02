from flask import Flask, request, Response, render_template, send_file
import os
from datetime import datetime

import cv2

from actuators import stepper
from sensors import mpu6050
from bot import robot
from sensors import camera
import RPi.GPIO as GPIO

from object_detection import detection

dir_path = os.path.dirname(os.path.realpath(__file__))
html_template_dir = os.path.join(dir_path, 'server')

app = Flask(__name__, template_folder=html_template_dir)

cam = camera.camera()

# Can be saved etc.
current_camera_picture_as_jpeg = None

#od = detection.Detector(model_path='object_detection/model/efficientdet_lite0.tflite',
#    max_results=5, score_threshold=0.3, camera_width=640, camera_height=480)

def init_robot():
    ####################################
    # Initializing sensors, motors, etc.
    ####################################
    front_left_stepper = stepper.stepper(
        DIR=11, STEP=9, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM, step_mode='1/32')

    front_right_stepper = stepper.stepper(
        DIR=10, STEP=22, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM, step_mode='1/32')

    back_left_stepper = stepper.stepper(
        DIR=19, STEP=13, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM, step_mode='1/32')

    back_right_stepper = stepper.stepper(
        DIR=6, STEP=5, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM, step_mode='1/32')

    lidar_stepper = stepper.stepper(
        DIR=16, STEP=20, SLP=21, steps_per_revolution=200, step_delay_seconds=0.005, activate_on_high=True, gpio_mode=GPIO.BCM)

    mpu = mpu6050.mpu6050()

    #od = detection.Detector(
    #        model_path='object_detection/model/efficientdet_lite0.tflite',
    #        max_results=200, score_threshold=0.3, camera_width=640, camera_height=480)

    return robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper, mpu, None, object_detection=None)

@app.route("/move")
def move():
    global bot
    direction = request.args.get('direction')
    if direction == 'forward':
        print('forward selected')
        bot.set_direction_forward()
    elif direction == 'backward':
        print('backward selected')
        bot.set_direction_backward()
    elif direction == 'verticalLeft':
        print('Vertical Left selected')
        bot.set_direction_vertical_left()
    elif direction == 'verticalRight':
        print('Vertical Right selected')
        bot.set_direction_vertical_right()
    bot.run_continuously_all_steppers()
    return "Moving"

@app.route("/stop")
def stop():
    global bot
    bot.stop_continously_all_steppers()
    return "Stopped"

@app.route("/turn")
def turn():
    direction = request.args.get('direction')
    global bot
    if direction == "left":
        bot.set_direction_left()
    elif direction == "right":
        bot.set_direction_right()
    else:
        return "Direction " + direction + " not supported. Choose either left or right."
    bot.run_continuously_all_steppers()
    return "Turning"


@app.route("/")
def remote():
    return render_template('remote.html')


def gen():
    """Video streaming generator function."""
    while True:
        global current_camera_picture_as_jpeg
        #global od
        #frame, result = bot.od.get_detected_objects_image_and_result()
        current_camera_picture_as_jpeg = cam.get_picture()
        ret, img = cv2.imencode('.jpg', current_camera_picture_as_jpeg)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img.tobytes() + b'\r\n')

@app.route("/save_picture")
def save_picture():
    print('In save_picture')
    global current_camera_picture_as_jpeg
    # dateTimeObj = datetime.now()
    # timestampStr = dateTimeObj.strftime("%Y-%m-%dT%H-%M-%S")
    folder = 'saved_pictures'
    file_name = 'tmp.jpg'
    abs_directory = os.path.join(app.root_path, folder)
    abs_file = os.path.join(abs_directory, file_name)
    cv2.imwrite(abs_file, current_camera_picture_as_jpeg)
    print('Saved picture: ', abs_file)
    return send_file(abs_file, as_attachment=True)

@app.route('/run_command')
def move_command():
    command = request.args.get('command')
    """Executes `execute_move_command` function of robot obj."""
    bot.execute_move_command(command)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    bot = init_robot()
    bot.deactivate_all_drive_steppers() # so that there is clearly no holding torque on the steppers

    app.run(host='0.0.0.0', port=5001)