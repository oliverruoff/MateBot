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

right_stepper.set_direction_clockwise(False)

left_stepper.turn_stepper_angle(3000, True, True)
right_stepper.turn_stepper_angle(3000, True, True)

time.sleep(3)

right_stepper.set_direction_clockwise(True)
left_stepper.set_direction_clockwise(False)

left_stepper.turn_stepper_angle(3000, True, True)
right_stepper.turn_stepper_angle(3000, True, True)

time.sleep(3)

left_stepper.deactivate_stepper()
right_stepper.deactivate_stepper()

