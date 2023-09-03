from roboflow import Roboflow
import cv2
import time
import sys

from src.config import PROJECT_WORKSPACE_ROBOFLOW, \
    API_KEY_ROBOFLOW, TITLE, FOLDER_PICTURE, NAME_PICTURE
from src.detector import Detector
from src.api import API


class Main:

    def __init__(self):
        self.detector = None
        self.actual_data_predict_picture: object = None
        self.cv2 = None
        self.rf = Roboflow(api_key=API_KEY_ROBOFLOW)
        self.project = self.rf.workspace().project(PROJECT_WORKSPACE_ROBOFLOW)
        self.model = self.project.version(2).model
        self.video = cv2.VideoCapture(0)
        self.one_hour: int = 60 * 60
        self.time_for_one_hour: float = time.time()
        self.latitude: float = float(sys.argv[1])
        self.longitude: float = float(sys.argv[2])
        self.city: str = sys.argv[3]
        self.api = API(self.city)
        self.run()

    def verif_time_one_hour(self) -> bool:
        if time.time() - self.time_for_one_hour > self.one_hour:
            self.time_for_one_hour = time.time()
            return True
        return False

    def take_picture(self):
        self.cv2.imwrite(FOLDER_PICTURE + NAME_PICTURE, self.video)

    def predict_picture(self):
        self.actual_data_predict_picture = self.model.predict(FOLDER_PICTURE +
                                                              NAME_PICTURE,
                                                              confidence=40,
                                                              overlap=30)\
            .json()
        self.model.predict(FOLDER_PICTURE + NAME_PICTURE,
                           confidence=40,
                           overlap=30).save(FOLDER_PICTURE + NAME_PICTURE)

    def run(self):
        while True:
            self.cv2.imshow(TITLE, self.video.read()[1])
            if self.cv2.waitKey(1) == ord('q'):
                break

            # ACTIONS

            if self.verif_time_one_hour():
                self.api.add_data_city(self.detector.get_nb_beach(),
                                       self.detector.get_nb_sea(),
                                       self.detector.get_visibility()),

            self.take_picture()
            self.predict_picture()
            self.api.add_picture_alert_or_moment(FOLDER_PICTURE + NAME_PICTURE)
            self.detector = Detector(self.actual_data_predict_picture)
            self.api.set_number_people(self.detector.get_nb_beach(),
                                       self.detector.get_nb_sea())

        self.video.release()
        cv2.destroyAllWindows()
