import time
import sys
import mysql.connector
import cv2
from ultralytics import YOLO

from config import FOLDER_PICTURE
from detector import Detector
from api import API
from alert import Alert
from city import City
from decimal import Decimal
from datetime import date, timedelta, datetime
import json


class Main:
    password: str
    user_name: str
    ip: str
    api: API
    latitude: float
    longitude: float
    city: str
    detector: Detector
    CITY: list[tuple[float |
                     int | Decimal | str | bytes | date |
                     timedelta | datetime | set[str] | bool |
                     None, ...]]
    alert: Alert
    actual_data_predict_picture: any
    one_hour: int
    time_for_one_hour: float
    OTHER_PROJECT_ROBOFLOW: list
    mydb: mysql.connector.connection.MySQLConnection
    time_start: float
    run_detection: bool
    run_blur: bool
    detector_id: int
    api_key: str
    launch_detection: str | None
    stop_detection: str | None

    def __init__(self):
        self.api_key = sys.argv[2]
        self.actual_data_predict_picture = None
        self.one_hour = 60 * 60
        self.time_for_one_hour = time.time()
        self.detector_id = int(sys.argv[7])
        self.mydb = mysql.connector.connect(
            host=sys.argv[3],
            user=sys.argv[4],
            password=sys.argv[5],
            port=sys.argv[6],
            database='C2SMR'
        )
        self.CITY = City(self.mydb, self.detector_id).return_city()
        self.model = YOLO("weight.pt")
        self.run()

    def verif_time_one_hour(self) -> bool:
        if time.time() - self.time_for_one_hour > self.one_hour:
            self.time_for_one_hour = time.time()
            return True
        return False

    def predict_picture(self, frame):
        results = self.model(frame)
        valid_results = []
        for r in results:
            if r is not None:
                try:
                    json_data = r.tojson()
                    if json_data is not None:
                        self.actual_data_predict_picture = json.loads(json_data)
                        valid_results.append(r)
                        break
                    else:
                        print(f"Résultat JSON vide pour l'image de {self.city}.")
                except AttributeError as e:
                    print(f"Erreur lors du traitement de l'image pour {self.city}: {e}")

        if not valid_results:
            print(f"Aucune détection valide pour l'image de {self.city}.")
            self.actual_data_predict_picture = None

    def set_value_for_city(self, index):
        self.CITY = City(self.mydb, self.detector_id).return_city()
        self.city = self.CITY[index][0]
        self.latitude = self.CITY[index][1]
        self.longitude = self.CITY[index][2]
        self.ip = self.CITY[index][3]
        self.user_name = self.CITY[index][4]
        self.password = self.CITY[index][5]
        self.run_detection = self.CITY[index][7]
        self.run_blur = self.CITY[index][6]
        self.launch_detection = self.CITY[index][8]
        self.stop_detection = self.CITY[index][9]

    def run(self):
        caps = []
        for city in self.CITY:
            rtsp_url = f"rtsp://{city[4]}:{city[5]}@{city[3]}:554/stream1"
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                print(f"Erreur: Impossible de connecter à la caméra de la ville {city[0]}.")
            else:
                caps.append(cap)

        if not caps:
            print("Erreur: Aucune caméra n'est disponible.")
            return

        while True:
            frames = []
            for cap in caps:
                ret, frame = cap.read()
                if not ret:
                    print(f"Erreur: Impossible de lire le flux vidéo de la caméra de la ville {self.city}.")
                    continue
                frames.append(frame)

            for i in range(len(self.CITY)):
                self.time_start = time.time()
                self.set_value_for_city(i)

                if self.run_detection:
                    if self.launch_detection is not None:
                        actual_hour = datetime.now().hour

                        if actual_hour < int(self.launch_detection) or \
                                actual_hour > int(self.stop_detection):
                            print(f'City: {self.city} pass')
                            continue
                    self.api = API(self.city, self.api_key, self.latitude, self.longitude)

                    for frame in frames:
                        self.predict_picture(frame)

                        self.detector = Detector(self.actual_data_predict_picture)

                        self.api.set_number_people(self.detector.get_nb_beach(),
                                                   self.detector.get_nb_sea())

                        self.alert = Alert(self.latitude, self.longitude,
                                           self.actual_data_predict_picture,
                                           self.api, self.city, self.mydb)
                        self.alert.run()

                        if self.verif_time_one_hour():
                            for j in range(len(self.CITY)):
                                self.set_value_for_city(j)
                                self.api = API(self.city, self.api_key,
                                               self.latitude, self.longitude)
                                self.api.add_data_city(self.detector.get_nb_beach(),
                                                       self.detector.get_nb_sea(),
                                                       self.detector.get_visibility())

                            self.set_value_for_city(i)

                        self.api.add_picture_alert_or_moment(FOLDER_PICTURE + self.city + '.png')
                        print(f'City: {self.city} has run in : {time.time() - self.time_start}')
                else:
                    print(f'City: {self.city} pass')

            for frame in frames:
                cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        for cap in caps:
            cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    Main()
