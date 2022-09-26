from actuators import stepper

import time
import RPi.GPIO as GPIO

####################################
# Initializing sensors, motors, etc.
####################################

left_stepper = stepper.stepper(
    DIR=4, STEP=3, SLP=2, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

right_stepper = stepper.stepper(
    DIR=11, STEP=9, SLP=10, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

right_stepper.turn_stepper_angle(360, False, True)

right_stepper.deactivate_stepper()

