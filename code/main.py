from actuators import stepper

import time
import RPi.GPIO as GPIO

####################################
# Initializing sensors, motors, etc.
####################################

front_left_stepper = stepper.stepper(
    DIR=4, STEP=3, SLP=2, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

front_right_stepper = stepper.stepper(
    DIR=11, STEP=9, SLP=10, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

back_left_stepper = stepper.stepper(
    DIR=26, STEP=19, SLP=13, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

back_right_stepper = stepper.stepper(
    DIR=21, STEP=20, SLP=16, steps_per_revolution=200, stepper_delay_seconds=0.0005, gpio_mode=GPIO.BCM)

front_right_stepper.turn_stepper_angle(360, False, False)

front_left_stepper.turn_stepper_angle(360, False, False)

back_left_stepper.turn_stepper_angle(360, False, False)

back_left_stepper.turn_stepper_angle(360, False, False)

# removing holding torque

front_right_stepper.deactivate_stepper()

front_left_stepper.deactivate_stepper()

back_right_stepper.deactivate_stepper()

back_left_stepper.deactivate_stepper()

