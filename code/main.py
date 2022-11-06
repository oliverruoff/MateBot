from actuators import stepper
from sensors import mpu6050
from bot import robot


import time
import RPi.GPIO as GPIO

try:

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

    robo = robot.Robot(front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper, lidar_stepper, mpu)

    # Setting stepper modes (e.g. to particular micro stepping mode)
    back_left_stepper.set_stepper_mode('1/32')
    back_right_stepper.set_stepper_mode('1/32')
    front_left_stepper.set_stepper_mode('1/32')
    front_right_stepper.set_stepper_mode('1/32')
    lidar_stepper.set_stepper_mode('Full')

    old_time = time.time()
    angle = 0

    while True:
            # Get angle from mpu sensor
            #ax = mpu.get_new_accel_angle('x')
            #ay = mpu.get_new_accel_angle('y')
            #az = mpu.get_new_accel_angle('z')
            
            new_time = time.time()

            #angle = mpu.get_new_gyro_angle('x', new_time - old_time, angle)

            #gy = mpu.get_new_gyro_angle('y', new_time - old_time)
            #gz = mpu.get_new_gyro_angle('z', new_time - old_time)

            old_time = new_time

            #rint('Accel: X:', int(ax), '\tY:', int(ay), '\tZ:',int(az), '\tGyro: X:', int(gx), '\tY:', int(gy), '\tZ:', int(gz))
            print('Angle:', mpu.get_full_accel_data)

            time.sleep(0.01)

    #lidar_stepper.turn_angle(90, False)
    #lidar_stepper.set_direction_clockwise(False)
    #lidar_stepper.turn_angle(180, False)
    #lidar_stepper.set_direction_clockwise(True)
    #lidar_stepper.turn_angle(90, False)

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
    lidar_stepper.deactivate_stepper()

except KeyboardInterrupt:

    # removing holding torque
    front_right_stepper.deactivate_stepper()
    front_left_stepper.deactivate_stepper()
    back_right_stepper.deactivate_stepper()
    back_left_stepper.deactivate_stepper()
    lidar_stepper.deactivate_stepper()

