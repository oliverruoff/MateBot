from actuators import stepper
from sensors import mpu6050
from bot import robot
from sensors import tfluna
from object_detection import detection


import time
import RPi.GPIO as GPIO

def init_robot():
    ####################################
    # Initializing sensors, motors, etc.
    ####################################
    front_left_stepper = stepper.stepper(
        DIR=11, STEP=9, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    front_right_stepper = stepper.stepper(
        DIR=10, STEP=22, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    back_left_stepper = stepper.stepper(
        DIR=19, STEP=13, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    back_right_stepper = stepper.stepper(
        DIR=6, STEP=5, SLP=26, steps_per_revolution=200, step_delay_seconds=0.00001, activate_on_high=False, gpio_mode=GPIO.BCM)

    lidar_stepper = stepper.stepper(
        DIR=16, STEP=20, SLP=21, steps_per_revolution=200, step_delay_seconds=0.005, activate_on_high=True, gpio_mode=GPIO.BCM)

    mpu = mpu6050.mpu6050()
    #tflu = tfluna.TFLuna()
    #lidar = lidar.lidar(lidar_stepper, tflu)

    return robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper, mpu, None)

try:
    robot = init_robot()

    # robot.lidar.scan_angle_with_stepper_position_reset(360)

    robot.follow_object(object_to_follow='person')

except KeyboardInterrupt:

    # removing holding torque
    robot.front_right_stepper.deactivate()
    robot.front_left_stepper.deactivate()
    robot.back_right_stepper.deactivate()
    robot.back_left_stepper.deactivate()
    robot.lidar.deactivate()

