import cv2


class camera:

    def __init__(self):
        pass

    def get_picture(self):
        cam = cv2.VideoCapture(0)
        s, image = cam.read()
        image = cv2.flip(image, flipCode=-1)
        return image
