import cv2


class CaptureCam:

    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def take_picture(self) -> None:
        cv2.imwrite('../../pictures/picture.jpg', self.video)

    def run(self) -> None:
        cv2.imshow("C2SMR", self.video.read()[1])
        self.take_picture()
        self.video.release()
        cv2.destroyAllWindows()
