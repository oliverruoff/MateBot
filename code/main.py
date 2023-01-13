from actuators import stepper
from sensors import mpu6050
from bot import robot
from sensors import tfluna
from object_detection import detection
from ina219 import INA219


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
    od = detection.Detector(
            model_path='object_detection/model/ssd_mobilenet_v1_1_metadata_1.tflite',
            max_results=5, score_threshold=0.3, camera_width=640, camera_height=480)

    return robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper, mpu, None, od)

try:
    rob = init_robot()

    rob.execute_move_command('f50,r90,f50,l45,b30', pause_seconds_between_commands=0.2)

    #while True:
    #    result = rob.od.detect_objects()
    #    print(result)
    #    time.sleep(1)

    #rob.set_direction_forward()
    #rob.run_continuously_all_steppers()
    #time.sleep(2)
    #rob.set_direction_backward()
    #time.sleep(2)
    #rob.set_direction_vertical_left()
    #time.sleep(2)
    #rob.set_direction_vertical_right()
    #time.sleep(2)
    #rob.stop_continously_all_steppers()


    # rob.lidar.scan_angle_with_stepper_position_reset(360)

    # rob.follow_object_continously()

except KeyboardInterrupt:

    # removing holding torque
    rob.front_right_stepper.deactivate()
    rob.front_left_stepper.deactivate()
    rob.back_right_stepper.deactivate()
    rob.back_left_stepper.deactivate()
    rob.lidar.deactivate()

