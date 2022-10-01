
class Robot:

    def __init__(self, front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper):
        self.front_left_stepper = front_left_stepper
        self.front_right_stepper = front_right_stepper
        self.back_left_stepper = back_left_stepper
        self.back_right_stepper = back_right_stepper

        self.position_X = 0
        self.position_Y = 0
        self.heading = 0

        self.TYRE_CIRCUMFERENCE_CM = 18.85              # manually determined
        self.ROBOT_CIRCUMFERENCE_CM = 157               # manually determined
        self.TURNING_ERROR_MULTIPLIER = 1               # manually determined

    def turn_all_steppers_angle(self, degree, asynch, ramping):
        if asynch:
            self.front_left_stepper.turn_stepper_angle(
                degree, True, ramping)
            self.front_right_stepper.turn_stepper_angle(
                degree, True, ramping)
            self.back_left_stepper.turn_stepper_angle(
                degree, True, ramping)
            self.back_right_stepper.turn_stepper_angle(
                degree, True, ramping)
        else:
            self.front_left_stepper.turn_stepper_angle(
                degree, True, ramping)
            self.front_right_stepper.turn_stepper_angle(
                degree, True, ramping)
            self.back_left_stepper.turn_stepper_angle(
                degree, True, ramping)
            self.back_right_stepper.turn_stepper_angle(
                degree, False, ramping)

    def drive_cm(self, cm, forward, ramping=False):
        if forward:
            self.front_left_stepper.set_direction_clockwise(False)
            self.front_right_stepper.set_direction_clockwise(True)
            self.back_left_stepper.set_direction_clockwise(False)
            self.back_right_stepper.set_direction_clockwise(True)
        else:
            self.front_left_stepper.set_direction_clockwise(True)
            self.front_right_stepper.set_direction_clockwise(False)
            self.back_left_stepper.set_direction_clockwise(True)
            self.back_right_stepper.set_direction_clockwise(False)
        desired_angle = (cm / self.TYRE_CIRCUMFERENCE_CM) * \
            360 * self.TURNING_ERROR_MULTIPLIER

        self.turn_all_steppers_angle(desired_angle, False, ramping)

    def turn_degree(self, degree, clockwise, ramping=False):
        if clockwise:
            self.front_left_stepper.set_direction_clockwise(False)
            self.front_right_stepper.set_direction_clockwise(False)
            self.back_left_stepper.set_direction_clockwise(False)
            self.back_right_stepper.set_direction_clockwise(False)
        else:
            self.front_left_stepper.set_direction_clockwise(True)
            self.front_right_stepper.set_direction_clockwise(True)
            self.back_left_stepper.set_direction_clockwise(True)
            self.back_right_stepper.set_direction_clockwise(True)

        desired_angle = (self.ROBOT_CIRCUMFERENCE_CM /
                         self.TYRE_CIRCUMFERENCE_CM) * degree * self.TURNING_ERROR_MULTIPLIER
        self.turn_all_steppers_angle(desired_angle, False, ramping)
        self.heading = (self.heading +
                        degree) % 360 if clockwise else (self.heading - degree) % -360