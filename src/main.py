from roboflow import Roboflow
import cv2
import time
import sys

from src.config import PROJECT_WORKSPACE_ROBOFLOW, \
    API_KEY_ROBOFLOW, TITLE, FOLDER_PICTURE, NAME_PICTURE


class Main:

    def __init__(self):
        self.actual_data_predict_picture = None
        self.cv2 = None
        self.rf = Roboflow(api_key=API_KEY_ROBOFLOW)
        self.project = self.rf.workspace().project(PROJECT_WORKSPACE_ROBOFLOW)
        self.model = self.project.version(2).model
        self.video = cv2.VideoCapture(0)
        self.one_hour = 60 * 60
        self.time_for_one_hour = time.time()
        self.latitude = sys.argv[1]
        self.longitude = sys.argv[2]

    def verif_time_one_hour(self):
        if time.time() - self.time_for_one_hour > self.one_hour:
            self.time_for_one_hour = time.time()

    def take_picture(self):
        self.cv2.imwrite(FOLDER_PICTURE + NAME_PICTURE, self.video)

    def predict_picture(self):
        self.actual_data_predict_picture = self.model.predict(FOLDER_PICTURE + NAME_PICTURE, confidence=40, overlap=30).json()
        self.model.predict(FOLDER_PICTURE + NAME_PICTURE, confidence=40, overlap=30).save(FOLDER_PICTURE + NAME_PICTURE)

    def run(self):
        while True:
            self.cv2.imshow(TITLE, self.video.read()[1])
            if self.cv2.waitKey(1) == ord('q'):
                break

            # ACTIONS

            self.verif_time_one_hour()
            self.take_picture()
            self.predict_picture()

        self.video.release()
        cv2.destroyAllWindows()
