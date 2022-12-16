from tflite_runtime.interpreter import Interpreter 
from PIL import Image
import numpy as np
import time

from sensors import camera

class Detector:

  def __init__(self, model_path, label_path):
    self.interpreter = self.init_interpreter(model_path)
    print("Model Loaded Successfully.")
    self.interpreter.allocate_tensors()
    _, self.height, self.width, _ = self.interpreter.get_input_details()[0]['shape']
    print("Image Shape (", self.width, ",", self.height, ")")
    # Read class labels.
    self.labels = self.load_labels(label_path)

  def init_interpreter(self, model_path):
    return Interpreter(model_path)
    

  def load_labels(self, path): # Read the labels from the text file as a Python list.
    with open(path, 'r') as f:
      return [line.strip() for i, line in enumerate(f.readlines())]

  def set_input_tensor(self, interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = image

  def classify_image(self, interpreter, image, top_k=1):
    self.set_input_tensor(interpreter, image)

    interpreter.invoke()
    output_details = interpreter.get_output_details()

    detection_boxes = interpreter.get_tensor(output_details[0]['index'])
    detection_classes = interpreter.get_tensor(output_details[1]['index'])
    detection_scores = interpreter.get_tensor(output_details[2]['index'])
    num_boxes = interpreter.get_tensor(output_details[3]['index'])
    print(num_boxes)
    for i in range(int(num_boxes[0])):
      if detection_scores[0, i] > .5:
          class_id = detection_classes[0, i]
          print(class_id, self.labels[class_id])

    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

    ordered = np.argpartition(-output, 1)
    return [(i, output[i]) for i in ordered[:top_k]][0]

  def detect_object(self):
    # Load an image to be classified.
    cam = camera.camera()
    image = cam.get_picture().convert('RGB').resize((self.width, self.height))

    # Classify the image.
    time1 = time.time()
    label_id, prob = self.classify_image(self.interpreter, image)
    time2 = time.time()
    classification_time = np.round(time2-time1, 3)
    print("Classificaiton Time =", classification_time, "seconds.")

    # Return the classification label of the image.
    classification_label = self.labels[label_id]
    print("Image Label is :", classification_label, ", with Accuracy :", np.round(prob*100, 2), "%.")