import time
import sys
import mysql.connector
import cv2
import os
from ultralytics import YOLO

from config import FOLDER_PICTURE
from detector import Detector
from api import API
from alert import Alert
from city import City
from scraper import Scraper
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
        self.dry_run = os.getenv('DRY', '0') == '1'
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
                        print(f"Pas de résultat {self.city}.")
                except AttributeError as e:
                    print(f"Erreur lors du traitement de l'image pour {self.city}: {e}")

        if not valid_results:
            print(f"Aucune détection valide pour l'image de {self.city}.")
            self.actual_data_predict_picture = None

    def set_value_for_city(self, index):
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
        print(len(self.CITY))
        print("aaaaaaaaaa")

        for city in self.CITY:
            print("bbbbbbbbbbb")
            rtsp_url = f"rtsp://admin:{city[5]}@{city[3]}/h264Preview_01_sub"
            print(city[5])
            print(rtsp_url)
            
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                print(f"Erreur: {city[0]}.")
            else:
                caps.append((cap, city[0]))

        if not caps:
            print("Erreur: Aucune caméra ")
            return

        while True:
            frames = []
            for cap, city_name in caps:
                cap.set(cv2.CAP_PROP_POS_MSEC, 1000) 
                ret, frame = cap.read()
                if not ret:
                    print(f"Erreur: Impossible de lire la caméra a {city_name}.")
                    continue
                frames.append((frame, city_name))

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

                    for frame, city_name in frames:
                        if city_name == self.city:
                            print(f"Processing frame for city: {self.city}")

                            (Scraper(self.city,
                             self.ip,
                             self.user_name,
                             self.password,
                             self.run_blur)
                     .get_picture(frame))
                            
                            
                            self.predict_picture(frame)

                            print('cccccccc')

                            self.detector = Detector(self.actual_data_predict_picture)

                            print('dddddddd')

                            self.api.set_number_people(self.detector.get_nb_beach(),
                                                       self.detector.get_nb_sea())
                            
                            print('eeeeeeeee')

                            #self.alert = Alert(self.latitude, self.longitude,
                            #                   self.actual_data_predict_picture,
                            #                   self.api, self.city, self.mydb)
                            #self.alert.run()

                            print('iiiiiiiiiiii')

                            if self.verif_time_one_hour():
                                for j in range(len(self.CITY)):
                                    self.set_value_for_city(j)
                                    print(f"Updating API data for city: {self.city}")
                                    self.api = API(self.city, self.api_key,
                                                   self.latitude, self.longitude)
                                    self.api.add_data_city(self.detector.get_nb_beach(),
                                                           self.detector.get_nb_sea(),
                                                           self.detector.get_visibility())

                                self.set_value_for_city(i)

                            self.api.add_picture_alert_or_moment(FOLDER_PICTURE + self.city + '.png')
                            print(f'City: {self.city} has run in : {time.time() - self.time_start}')

                            print('fffffffffff')
                else:
                    print(f'City: {self.city} pass')

            if not self.dry_run:
                image_path = "./picture/Villers-sur-mer.png"
                image = cv2.imread(image_path)
                if image is not None:
                    cv2.imshow('Video', image)
                else:
                    print("Pas d'image")

                if cv2.waitKey(1) & 0xFF == ord('a'):
                    break

        for cap, _ in caps:
            cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    Main()
