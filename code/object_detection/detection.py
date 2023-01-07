from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
from object_detection import utils

from sensors import camera

class Detector:

  def __init__(self, model_path='object_detection/model/efficientdet_lite0.tflite',
    max_results=200, score_threshold=0.3, camera_width=640, camera_height=480):

    self.cam = camera.camera(width=camera_width, height=camera_height)

    # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model_path, use_coral=False, num_threads=4)
    detection_options = processor.DetectionOptions(
        max_results=max_results, score_threshold=score_threshold)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    self.detector = vision.ObjectDetector.create_from_options(options)


  def detect_objects(self):
    """Detecting objects returning result

    Returns:
        DetectionResult: List of detected objects
    """
    image = self.cam.get_picture()

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(image)

    # Run object detection estimation using the model.
    return self.detector.detect(input_tensor)

  def get_detected_objects_image_and_result(self):
    """Detecting objects returning image with bounding boxes

    Returns:
        cv2.Image: Image including bounding boxes
    """

    image = self.cam.get_picture()

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(image)

    # Run object detection estimation using the model.
    detection_result = self.detector.detect(input_tensor)
    # Draw keypoints and edges on input image
    image = utils.visualize(image, detection_result)

    return image, detection_result