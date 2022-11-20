from flask import Flask, request, Response, render_template
import os

import cv2

from actuators import stepper
from sensors import mpu6050
from bot import robot
import RPi.GPIO as GPIO

dir_path = os.path.dirname(os.path.realpath(__file__))
html_template_dir = os.path.join(dir_path, 'server')

app = Flask(__name__, template_folder=html_template_dir)
vc = cv2.VideoCapture(0)

def init_robot():
    ####################################
    # Initializing sensors, motors, etc.
    ####################################
    front_left_stepper = stepper.stepper(
        DIR=11, STEP=9, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    front_right_stepper = stepper.stepper(
        DIR=10, STEP=22, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    back_left_stepper = stepper.stepper(
        DIR=19, STEP=13, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    back_right_stepper = stepper.stepper(
        DIR=6, STEP=5, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    lidar_stepper = stepper.stepper(
        DIR=16, STEP=20, SLP=21, steps_per_revolution=200, stepper_delay_seconds=0.005, activate_on_high=True, gpio_mode=GPIO.BCM)

    mpu = mpu6050.mpu6050()

    return robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper, lidar_stepper, mpu)

def get_frequency_for_percent(percent):
    if percent < 11:
            left = 320
    elif percent > 11 and percent < 22:
        left = 400
    elif percent > 22 and percent < 33:
        left = 500
    elif percent > 33 and percent < 44:
        left = 800
    elif percent > 44 and percent < 55:
        left = 1000
    elif percent > 55 and percent < 66:
        left = 1600
    elif percent > 66 and percent < 77:
        left = 2000
    elif percent > 77 and percent < 88:
        left = 4000
    elif percent > 88 :
        left = 8000

@app.route("/joystick")
def joystick():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))

    print('x:', x)
    print('y:', y)
    abs_y = abs(y)
    abs_x = abs(x)
    if x == 0 and y == 0:
        bot.deactivate_all_drive_steppers()
        return 'Stopped motors.'

    if y > 0:
        bot.set_direction_forward()
    elif y < 0:
        bot.set_direction_backward()
    else:
        bot.deactivate_all_drive_steppers()

    if x > 0:
        left = get_frequency_for_percent(abs_y)
        right = get_frequency_for_percent(int(abs_y - (abs_x*(abs_y/100))))
    elif x < 0:
        right = get_frequency_for_percent(abs_y)
        left = get_frequency_for_percent(int(abs_y - (abs_x*(abs_y/100))))
    else:
        return "Error: x value seems to be strange: " + x
    print('left:', left, 'right:', right)
    bot.front_left_stepper.run_continuously(frequency=right)
    bot.front_left_stepper.run_continuously(frequency=left)
    return 'Done'


@app.route("/joystickscript")
def joystickscript():
    return js_str


@app.route("/")
def remote():
    return render_template('remote.html', js_path=js_path)


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
    
    bot = init_robot()
    bot.deactivate_all_drive_steppers() # so that there is clearly no holding torque on the steppers

    # remote_html = prepare_remote()
    js_path = os.path.join(dir_path, 'server', 'joystick.js')
    with open(js_path, 'r') as file:
        js_str = file.read()

    app.run(host='0.0.0.0', port=5001)