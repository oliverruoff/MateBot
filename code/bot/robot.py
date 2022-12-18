import math
import time

from object_detection import detection

class Robot:

    def __init__(self, front_left_stepper, front_right_stepper, back_left_stepper, back_right_stepper, mpu, lidar):
        self.front_left_stepper = front_left_stepper
        self.front_right_stepper = front_right_stepper
        self.back_left_stepper = back_left_stepper
        self.back_right_stepper = back_right_stepper
        self.mpu = mpu
        self.lidar = lidar
        self.camera_width = 160
        self.camera_height = 120
        self.od = detection.Detector(
            model_path='object_detection/model/efficientdet_lite0.tflite',
            max_results=5, score_threshold=0.3, camera_width=self.camera_width, camera_height=self.camera_height)

        self.position_X = 0
        self.position_Y = 0
        self.heading = 0

        self.TYRE_CIRCUMFERENCE_CM = math.pi * 8          # manually determined
        self.ROBOT_CIRCUMFERENCE_CM = math.pi * 50        # manually determined
        self.TURNING_ERROR_MULTIPLIER = 1.36              # manually determined

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
                        pass
                    elif object_center > self.camera_width/2 and turn_related_to_offset > move_threshold:
                        print(object_to_follow, 'is to my right. Moving: ',turn_related_to_offset,'°')
                        self.turn_degree_gyro_supported(turn_related_to_offset, True)
                    else:
                        print(object_to_follow, 'seems to be right in front of me.')



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
