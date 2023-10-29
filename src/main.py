from roboflow import Roboflow
import time
import sys

from config import PROJECT_WORKSPACE_ROBOFLOW, \
    API_KEY_ROBOFLOW, FOLDER_PICTURE, NAME_PICTURE
from detector import Detector
from api import API
from alert import Alert
from capture.chrome.main import Navigation
from capture.opencv.main import CaptureCam


class Main:

    def __init__(self):
        self.detector = None
        self.alert = None
        self.sensors = None
        self.actual_data_predict_picture: object = None
        self.cv2 = None
        self.rf = Roboflow(api_key=API_KEY_ROBOFLOW)
        self.project = self.rf.workspace().project(PROJECT_WORKSPACE_ROBOFLOW)
        self.model = self.project.version(int(sys.argv[5])).model
        self.one_hour: int = 60 * 60
        self.time_for_one_hour: float = time.time()
        self.latitude: float = float(sys.argv[1])
        self.longitude: float = float(sys.argv[2])
        self.city: str = sys.argv[3].replace('_', ' ')
        self.type_of_cam: str = sys.argv[4]
        self.api: API = API(self.city, sys.argv[6],
                            self.latitude, self.longitude)
        if self.type_of_cam != "":
            self.sensors = Navigation(self.type_of_cam)
        else:
            self.sensors = CaptureCam()

        self.run()

    def verif_time_one_hour(self) -> bool:
        if time.time() - self.time_for_one_hour > self.one_hour:
            self.time_for_one_hour = time.time()
            return True
        return False

    def predict_picture(self):
        self.actual_data_predict_picture = self.model.predict(FOLDER_PICTURE +
                                                              NAME_PICTURE,
                                                              confidence=40,
                                                              overlap=30) \
            .json()
        self.model.predict(FOLDER_PICTURE + NAME_PICTURE,
                           confidence=40,
                           overlap=30).save(FOLDER_PICTURE + NAME_PICTURE)

    def run(self):
        while True:

            # CAPTURES
            self.sensors.run()

            # ACTIONS

            if self.verif_time_one_hour():
                self.api.add_data_city(self.detector.get_nb_beach(),
                                       self.detector.get_nb_sea(),
                                       self.detector.get_visibility()),

            self.predict_picture()
            self.detector: Detector = Detector(
                self.actual_data_predict_picture)
            self.api.set_number_people(self.detector.get_nb_beach(),
                                       self.detector.get_nb_sea())
            self.alert: Alert = Alert(self.latitude, self.longitude,
                                      self.actual_data_predict_picture,
                                      self.api)
            self.alert.run()
            # self.api.add_picture_alert_or_moment(
            # FOLDER_PICTURE + NAME_PICTURE)


if __name__ == '__main__':
    Main()
