from flask import Flask, request, Response
import cv2
import RPi.GPIO as GPIO

from actuators import stepper
from sensors import mpu6050
from bot import robot


app = Flask(__name__)
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

@app.route("/health")
def health():
    return "I'm alive!"

@app.route("/move_cm")
def move_cm():
    forward = bool(request.args.get('forward'))
    cm = float(request.args.get('cm'))
    # TODO: Implement
    return "Moved."

@app.route("/move")
def move():
    global bot
    forward = bool(request.args.get('forward'))
    if forward:
        bot.set_direction_forward()
    else:
        bot.set_direction_backward()
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
    app.run(host='0.0.0.0', port=5000)