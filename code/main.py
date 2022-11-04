from actuators import stepper
from bot import robot

import time
import RPi.GPIO as GPIO

try:

    ####################################
    # Initializing sensors, motors, etc.
    ####################################
    front_left_stepper = stepper.stepper(
        DIR=11, STEP=9, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, gpio_mode=GPIO.BCM)

    front_right_stepper = stepper.stepper(
        DIR=10, STEP=22, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, gpio_mode=GPIO.BCM)

    back_left_stepper = stepper.stepper(
        DIR=19, STEP=13, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, gpio_mode=GPIO.BCM)

    back_right_stepper = stepper.stepper(
        DIR=6, STEP=5, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.00001, gpio_mode=GPIO.BCM)

    robo = robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper)

    back_left_stepper.set_stepper_mode('1/32')
    back_right_stepper.set_stepper_mode('1/32')
    front_left_stepper.set_stepper_mode('1/32')
    front_right_stepper.set_stepper_mode('1/32')
    '''
    front_left_stepper.set_direction_clockwise(False)
    back_left_stepper.set_direction_clockwise(False)

    back_left_stepper.turn_angle(720, True)
    back_right_stepper.turn_angle(720, True)
    front_left_stepper.turn_angle(720, True)
    front_right_stepper.turn_angle(720, False)

    front_left_stepper.set_direction_clockwise(True)
    back_left_stepper.set_direction_clockwise(True)
    front_right_stepper.set_direction_clockwise(False)
    back_right_stepper.set_direction_clockwise(False)

    back_left_stepper.turn_angle(720, True)
    back_right_stepper.turn_angle(720, True)
    front_left_stepper.turn_angle(720, True)
    front_right_stepper.turn_angle(720, False)

    front_right_stepper.set_direction_clockwise(True)
    back_right_stepper.set_direction_clockwise(True)

    back_left_stepper.turn_angle(720, True)
    back_right_stepper.turn_angle(720, True)
    front_left_stepper.turn_angle(720, True)
    front_right_stepper.turn_angle(720, False)

    front_left_stepper.set_direction_clockwise(False)
    back_left_stepper.set_direction_clockwise(False)
    front_right_stepper.set_direction_clockwise(False)
    back_right_stepper.set_direction_clockwise(False)

    back_left_stepper.turn_angle(720, True)
    back_right_stepper.turn_angle(720, True)
    front_left_stepper.turn_angle(720, True)
    front_right_stepper.turn_angle(720, False)'''

    robo.drive_cm(50, True)
    robo.turn_degree(90, True)
    robo.drive_cm(50, True)
    robo.turn_degree(90, True)
    robo.drive_cm(50, True)
    robo.turn_degree(90, True)
    robo.drive_cm(50, True)
    robo.turn_degree(90, True)

    front_right_stepper.deactivate_stepper()
    front_left_stepper.deactivate_stepper()
    back_right_stepper.deactivate_stepper()
    back_left_stepper.deactivate_stepper()

except KeyboardInterrupt:

    # removing holding torque
    front_right_stepper.deactivate_stepper()
    front_left_stepper.deactivate_stepper()
    back_right_stepper.deactivate_stepper()
    back_left_stepper.deactivate_stepper()

