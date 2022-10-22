from actuators import stepper
from bot import robot

import time
import RPi.GPIO as GPIO

try:

    ####################################
    # Initializing sensors, motors, etc.
    ####################################
    front_left_stepper = stepper.stepper(
        DIR=19, STEP=13, SLP=26, steps_per_revolution=200, stepper_delay_seconds=0.005, gpio_mode=GPIO.BCM)

    front_left_stepper.set_direction_clockwise()

    #front_left_stepper.run_continuously()
    #time.sleep(2)
    #front_left_stepper.stop_continuous()

    front_left_stepper.turn_stepper_angle(360, False, False)

    #front_right_stepper = stepper.stepper(
    #    DIR=11, STEP=9, SLP=10, M0=7, M1=8, M2=25, steps_per_revolution=200, stepper_delay_seconds=0.00001, gpio_mode=GPIO.BCM)

    #back_left_stepper = stepper.stepper(
     #   DIR=26, STEP=19, SLP=13, M0=7, M1=8, M2=25, steps_per_revolution=200, stepper_delay_seconds=0.00001, gpio_mode=GPIO.BCM)

    #back_right_stepper = stepper.stepper(
    #    DIR=21, STEP=20, SLP=16, M0=7, M1=8, M2=25, steps_per_revolution=200, stepper_delay_seconds=0.00001, gpio_mode=GPIO.BCM)

    #robo = robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper)

    
    #robo.drive_cm(50, True)
    #robo.turn_degree(90, True)
    #robo.drive_cm(50, True)
    #robo.turn_degree(90, True)
    #robo.drive_cm(50, True)
    #robo.turn_degree(90, True)
    #robo.drive_cm(50, True)
    #robo.turn_degree(90, True)

    #front_right_stepper.deactivate_stepper()
    #front_left_stepper.deactivate_stepper()
    #back_right_stepper.deactivate_stepper()
    #back_left_stepper.deactivate_stepper()

except KeyboardInterrupt:

    # removing holding torque
    #front_right_stepper.deactivate_stepper()
    front_left_stepper.deactivate_stepper()
    #back_right_stepper.deactivate_stepper()
    #back_left_stepper.deactivate_stepper()

