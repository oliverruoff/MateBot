import cv2
from PIL import Image

class camera:



    def __init__(self):
        self.width = 640
        self.height = 480

    def get_picture(self):
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        s, image = cam.read()
        image = cv2.flip(image, flipCode=-1)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        return image
