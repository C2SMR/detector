import cv2

from src.config import TITLE, FOLDER_PICTURE, NAME_PICTURE


class Main:

    def __init__(self):
        self.cv2 = None
        self.video = cv2.VideoCapture(0)
        self.run()

    def take_picture(self):
        self.cv2.imwrite('../..' + FOLDER_PICTURE + NAME_PICTURE, self.video)

    def run(self):
        while True:
            self.cv2.imshow(TITLE, self.video.read()[1])
            if self.cv2.waitKey(1) == ord('q'):
                break

            self.take_picture()

        self.video.release()
        cv2.destroyAllWindows()
