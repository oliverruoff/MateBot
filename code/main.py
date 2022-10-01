from actuators import stepper
from bot import robot

import time
import RPi.GPIO as GPIO

try:

    
    ####################################
    # Initializing sensors, motors, etc.
    ####################################
    front_left_stepper = stepper.stepper(
        DIR=4, STEP=3, SLP=2, M0=7, M1=8, M2=25, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

    front_right_stepper = stepper.stepper(
        DIR=11, STEP=9, SLP=10, M0=7, M1=8, M2=25, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

    back_left_stepper = stepper.stepper(
        DIR=26, STEP=19, SLP=13, M0=7, M1=8, M2=25, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

    back_right_stepper = stepper.stepper(
        DIR=21, STEP=20, SLP=16, M0=7, M1=8, M2=25, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

    front_left_stepper.set_stepper_mode('1/32')
    front_right_stepper.set_stepper_mode('1/32')
    back_left_stepper.set_stepper_mode('1/32')
    back_right_stepper.set_stepper_mode('1/32')

    robo = robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper)

    
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

