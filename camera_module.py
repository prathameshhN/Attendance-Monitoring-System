import cv2

class CameraModule:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def capture_image(self):
        ret, img = self.cap.read()
        return img