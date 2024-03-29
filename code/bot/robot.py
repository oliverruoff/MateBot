import math
import time

from object_detection import detection

class Robot:

    def __init__(self, front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper, mpu, lidar, object_detection):
        self.front_left_stepper = front_left_stepper
        self.front_right_stepper = front_right_stepper
        self.back_left_stepper = back_left_stepper
        self.back_right_stepper = back_right_stepper
        self.mpu = mpu
        self.lidar = lidar
        self.camera_width = 640
        self.camera_height = 480
        self.od = object_detection 
        self.position_X = 0
        self.position_Y = 0
        self.heading = 0

        self.TYRE_CIRCUMFERENCE_CM = math.pi * 8          # manually determined
        self.ROBOT_CIRCUMFERENCE_CM = math.pi * 50        # manually determined
        self.TURNING_ERROR_MULTIPLIER = 1                 # manually determined

    def set_direction_left(self):
        self.front_left_stepper.set_direction_clockwise(True)
        self.front_right_stepper.set_direction_clockwise(True)
        self.back_left_stepper.set_direction_clockwise(True)
        self.back_right_stepper.set_direction_clockwise(True)

    def set_direction_right(self):
        self.front_left_stepper.set_direction_clockwise(False)
        self.front_right_stepper.set_direction_clockwise(False)
        self.back_left_stepper.set_direction_clockwise(False)
        self.back_right_stepper.set_direction_clockwise(False)

    def set_direction_forward(self):
        self.front_left_stepper.set_direction_clockwise(False)
        self.front_right_stepper.set_direction_clockwise(True)
        self.back_left_stepper.set_direction_clockwise(False)
        self.back_right_stepper.set_direction_clockwise(True)

    def set_direction_backward(self):
        self.front_left_stepper.set_direction_clockwise(True)
        self.front_right_stepper.set_direction_clockwise(False)
        self.back_left_stepper.set_direction_clockwise(True)
        self.back_right_stepper.set_direction_clockwise(False)

    def set_direction_vertical_right(self):
        self.back_right_stepper.set_direction_clockwise(True)
        self.back_left_stepper.set_direction_clockwise(True)
        self.front_right_stepper.set_direction_clockwise(False)
        self.front_left_stepper.set_direction_clockwise(False)

    def set_direction_vertical_left(self):
        self.back_right_stepper.set_direction_clockwise(False)
        self.back_left_stepper.set_direction_clockwise(False)
        self.front_right_stepper.set_direction_clockwise(True)
        self.front_left_stepper.set_direction_clockwise(True)

    def follow_object_continously(self, object_to_follow='person'):
        while True:
            self.follow_object_one_step(object_to_follow, self.od.detect_objects())

    def follow_object_one_step(self, object_to_follow, object_detection_result):
        move_threshold = 5 # degree
        print('Looking for:', object_to_follow)
        for detection in object_detection_result.detections:
            for category in detection.categories:
                print('Detected: ', category.category_name)
                if category.category_name == object_to_follow:
                    print('Object detected:', object_to_follow)
                    bounding_box_origin_x = detection.bounding_box.origin_x
                    bounding_box_width = detection.bounding_box.width
                    bounding_box_height = detection.bounding_box.height
                    object_center = bounding_box_origin_x + bounding_box_width/2
                    offset_from_center = abs(object_center - self.camera_width/2)
                    turn_related_to_offset = offset_from_center / 4
                    print('Obj_Center:', object_center, 'Obj_Offset:', offset_from_center, 'Turn:', turn_related_to_offset)
                    if object_center < self.camera_width/2 and turn_related_to_offset > move_threshold:
                        print(object_to_follow, 'is to my left. Moving: ',turn_related_to_offset,'°')
                        self.turn_degree_gyro_supported(turn_related_to_offset, False)
                    elif object_center > self.camera_width/2 and turn_related_to_offset > move_threshold:
                        print(object_to_follow, 'is to my right. Moving: ',turn_related_to_offset,'°')
                        self.turn_degree_gyro_supported(turn_related_to_offset, True)
                    else:
                        print(object_to_follow, 'seems to be right in front of me.')

    def turn_all_steppers_angle_v2(self, degree):
        self.front_left_stepper.activate()
        self.front_right_stepper.activate()
        self.back_left_stepper.activate()
        self.back_right_stepper.activate()
        steps = self.front_left_stepper.get_steps_for_angle(degree)
        for _ in range(steps):
            self.front_left_stepper.step_high()
            self.front_right_stepper.step_high()
            self.back_left_stepper.step_high()
            self.back_right_stepper.step_high()
            time.sleep(self.front_left_stepper.step_delay_seconds)
            self.front_left_stepper.step_low()
            self.front_right_stepper.step_low()
            self.back_left_stepper.step_low()
            self.back_right_stepper.step_low()
            time.sleep(self.front_left_stepper.step_delay_seconds)
        self.front_left_stepper.deactivate()
        self.front_right_stepper.deactivate()
        self.back_left_stepper.deactivate()
        self.back_right_stepper.deactivate()

    def turn_all_steppers_angle(self, degree, asynch, ramping):
        if asynch:
            self.front_left_stepper.turn_angle(
                degree, True, ramping)
            self.front_right_stepper.turn_angle(
                degree, True, ramping)
            self.back_left_stepper.turn_angle(
                degree, True, ramping)
            self.back_right_stepper.turn_angle(
                degree, True, ramping)
        else:
            self.front_left_stepper.turn_angle(
                degree, True, ramping)
            self.front_right_stepper.turn_angle(
                degree, True, ramping)
            self.back_left_stepper.turn_angle(
                degree, True, ramping)
            self.back_right_stepper.turn_angle(
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

        print('<drive_cm> Desired_angle for all steppers:', desired_angle)

        self.turn_all_steppers_angle_v2(desired_angle)

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
        self.turn_all_steppers_angle_v2(desired_angle)
        self.heading = (self.heading +
                        degree) % 360 if clockwise else (self.heading - degree) % -360

    def run_continuously_all_steppers(self):
        self.front_left_stepper.run_continuously()
        self.front_right_stepper.run_continuously()
        self.back_left_stepper.run_continuously()
        self.back_right_stepper.run_continuously()

    def stop_continously_all_steppers(self):
        self.front_left_stepper.stop_continuous()
        self.front_right_stepper.stop_continuous()
        self.back_left_stepper.stop_continuous()
        self.back_right_stepper.stop_continuous()

    def deactivate_all_drive_steppers(self):
        self.front_left_stepper.deactivate()
        self.front_right_stepper.deactivate()
        self.back_left_stepper.deactivate()
        self.back_right_stepper.deactivate()

    def turn_degree_gyro_supported(self, degree, clockwise):
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

        old_time = time.time()
        current_angle = 0
        desired_angle = degree
        self.run_continuously_all_steppers()
        while abs(current_angle) < desired_angle:
            new_time = time.time()
            # Get angle from mpu sensor
            current_angle = self.mpu.get_new_gyro_angle('x', new_time - old_time, current_angle)
            old_time = new_time
            time.sleep(0.01)

        self.stop_continously_all_steppers()

        self.heading = (self.heading +
                        degree) % 360 if clockwise else (self.heading - degree) % -360

    def execute_move_command(self, move_command, pause_seconds_between_commands=0):
        """Executes a move command which is put together by commas and which the roboter then will
        execute step by step.
        There are four chars allowed: f (forward), b (backward), r (right), l (left).
        After each char there has to come an integer. For f and b this will be the cm,
        the roboter has to drive in the given direction. For r and l this will be degree,
        to which the roboter has to turn in the given direction.

        E.g.: move_command = "f10,r90,b210,l180"
        With this command, the robot will move 10cm forward, then turn 90 degree to its right,
        then drive 210cm backward and finally turn 180 degree to its left.

        Args:
            move_command (str): Command, split by commas. E.g.: "f10,r90,b210,l180"
            pause_seconds_between_commands (int): Will pause this number of seconds between executing commands (defaults: 0)
        """
        for command in move_command.split(','):
            mode = command[:1]
            degree_or_cm = int(command[1:])
            if mode == 'f':
                print('Driving', degree_or_cm, 'cm forward.')
                self.drive_cm(degree_or_cm, True)
            elif mode == 'b':
                print('Driving', degree_or_cm, 'cm backward.')
                self.drive_cm(degree_or_cm, False)
            elif mode == 'l':
                print('Turning', degree_or_cm, 'to my left.')
                self.turn_degree_gyro_supported(degree_or_cm, False)  
            elif mode == 'r':
                print('Turning', degree_or_cm, 'to my right.')
                self.turn_degree_gyro_supported(degree_or_cm, True)
            else:
                print('Mode:', mode, 'is not supported! Skipping this command.')
            time.sleep(pause_seconds_between_commands)
        self.stop_continously_all_steppers()

    def search_object(self, object_to_search, min_score=0.38):
        """Looking for an object using the object detection model in the od obj. for this robot.
        The object to search should be a category in that object detection model.
        Example: `anchorpoint`. It will try to detect it, if it's not detected, it will turn
        60° clockwise. If it detects multiple objects of the searched category, it will focus on the
        one with the highest score. And then try to turn the robot to it. 
        Stops when it's close to centering it (x_diff < self.camera_width/20).

        Args:
            object_to_search (str): Category appearing in the object detection model used.
            min_score (float): Minimal score the object should have, else it's not respected.
        """
        aim_detection = None
        max_score = 0
        detections = self.od.get_detected_objects_image_and_result()[1].detections
        for d in detections:
            c = d.categories[0]
            if c.category_name == object_to_search:
                if c.score > max_score:
                    max_score = c.score
                    aim_detection = d
        if aim_detection == None or max_score < min_score:
            print('No', object_to_search, 'found, turning.')
            self.turn_degree_gyro_supported(degree=60, clockwise=True)
            self.search_object(object_to_search)
        else:
            print(object_to_search, 'with highest score:', aim_detection)
            bb_center = aim_detection.bounding_box.origin_x + (aim_detection.bounding_box.width/2)
            x_diff = (self.camera_width/2) - bb_center
            if abs(x_diff) < self.camera_width/15: # divisor defines tolerance. --> smaller means bigger tolerance
                print(object_to_search, 'seems to be right in front of me')
            else:
                direction_clockwise = True if x_diff < 0 else False
                print('Turning for', x_diff/10, 'clockwise:', direction_clockwise)
                self.turn_degree_gyro_supported(degree=abs(x_diff/10), clockwise=direction_clockwise)
                self.search_object(object_to_search)

        