import cv2

class camera:



    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

    def get_picture(self):
        cam = cv2.VideoCapture(-1)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        s, image = cam.read()
        image = cv2.flip(image, flipCode=-1)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        return image
