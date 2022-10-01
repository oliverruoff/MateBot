from actuators import stepper

import time
import RPi.GPIO as GPIO

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

#front_left_stepper.set_stepper_mode('1/16')
#front_right_stepper.set_stepper_mode('Full')
#back_left_stepper.set_stepper_mode('1/16')
#back_right_stepper.set_stepper_mode('1/16')

#front_left_stepper.set_direction_clockwise(False)
#back_left_stepper.set_direction_clockwise(False)

#front_right_stepper.run_continuously(frequency=500)
#front_left_stepper.run_continuously(frequency=500)
#back_right_stepper.run_continuously(frequency=500)
#back_left_stepper.run_continuously(frequency=500)

#time.sleep(2)

#front_right_stepper.turn_stepper_angle(360, False, False)

#front_right_stepper.stop_continuous()
#front_left_stepper.stop_continuous()
#back_right_stepper.stop_continuous()
#back_left_stepper.stop_continuous()


# removing holding torque

front_right_stepper.activate_stepper()

front_left_stepper.activate_stepper()

back_right_stepper.activate_stepper()

back_left_stepper.activate_stepper()

#front_right_stepper.deactivate_stepper()

#front_left_stepper.deactivate_stepper()

#back_right_stepper.deactivate_stepper()

#back_left_stepper.deactivate_stepper()

