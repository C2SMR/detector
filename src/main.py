from roboflow import Roboflow
import time
import sys

from config import PROJECT_WORKSPACE_ROBOFLOW, \
    FOLDER_PICTURE
from detector import Detector
from api import API
from alert import Alert
from city import CITY
from scraper import Scraper


class Main:

    def __init__(self):
        self.password = None
        self.user_name = None
        self.ip = None
        self.api = None
        self.latitude = None
        self.longitude = None
        self.city = None
        self.detector = None
        self.alert = None
        self.actual_data_predict_picture = None
        self.api_key: str = sys.argv[2]
        self.rf: Roboflow = Roboflow(api_key="rBzJE5DXKnwjcrNDnOxw")
        self.project = self.rf.workspace().project(PROJECT_WORKSPACE_ROBOFLOW)
        self.model = self.project.version(int(sys.argv[1])).model
        self.one_hour: int = 60 * 60
        self.time_for_one_hour: float = time.time()
        self.OTHER_PROJECT_ROBOFLOW: list = [
            Roboflow(api_key="rBzJE5DXKnwjcrNDnOxw").workspace()
            .project("drowning-detection-oxcyt")
            .version(1).model
        ]

        self.run()

    def verif_time_one_hour(self) -> bool:
        if time.time() - self.time_for_one_hour > self.one_hour:
            self.time_for_one_hour = time.time()
            return True
        return False

    def predict_picture(self):
        self.actual_data_predict_picture = self.model.predict(FOLDER_PICTURE +
                                                              self.city
                                                              + '.png',
                                                              confidence=40,
                                                              overlap=30) \
            .json()
        self.model.predict(FOLDER_PICTURE + self.city + '.png',
                           confidence=40,
                           overlap=30).save(FOLDER_PICTURE + self.city
                                            + '.png')

        for project in self.OTHER_PROJECT_ROBOFLOW:
            prediction = project.predict(FOLDER_PICTURE +
                                         self.city + '.png',
                                         confidence=40,
                                         overlap=30).json()
            for pred in prediction['predictions']:
                self.actual_data_predict_picture['predictions'].append(pred)

            project.predict(FOLDER_PICTURE +
                            self.city + '.png',
                            confidence=40,
                            overlap=30).save(FOLDER_PICTURE +
                                             self.city + '.png')

    def set_value_for_city(self, index):
        self.city: str = CITY[index][0]
        self.latitude: float = CITY[index][1]
        self.longitude: float = CITY[index][2]
        self.ip: str = CITY[index][3]
        self.user_name: str = CITY[index][4]
        self.password: str = CITY[index][5]

    def run(self):
        while True:

            for i in range(len(CITY)):
                self.set_value_for_city(i)
                self.api: API = API(self.city, self.api_key,
                                    self.latitude, self.longitude)
                (Scraper(self.city, self.ip, self.user_name, self.password)
                 .get_picture())
                self.predict_picture()
                self.detector: Detector = Detector(
                    self.actual_data_predict_picture)

                self.api.set_number_people(self.detector.get_nb_beach(),
                                           self.detector.get_nb_sea())
                self.alert: Alert = Alert(self.latitude, self.longitude,
                                          self.actual_data_predict_picture,
                                          self.api)
                self.alert.run()

                if self.verif_time_one_hour():
                    for j in range(len(CITY)):
                        self.set_value_for_city(j)

                        self.api: API = API(self.city, self.api_key,
                                            self.latitude, self.longitude)
                        self.api.add_data_city(self.detector.get_nb_beach(),
                                               self.detector.get_nb_sea(),
                                               self.detector.get_visibility()),
                    self.set_value_for_city(i)
                self.api.add_picture_alert_or_moment(
                    FOLDER_PICTURE + self.city + '.png')


if __name__ == '__main__':
    Main()
