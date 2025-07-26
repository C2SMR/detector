import os
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
    CITY: list[
        tuple[
            float
            | int
            | Decimal
            | str
            | bytes
            | date
            | timedelta
            | datetime
            | set[str]
            | bool
            | None,
            ...,
        ]
    ]
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
    type_detection = None
    public_url: str | None
    save_picture: bool

    def __init__(self):
        self.api_key = sys.argv[2]
        self.actual_data_predict_picture = None
        self.one_hour = 60 * 60
        self.time_for_one_hour = time.time()
        self.detector_id = int(sys.argv[3])
        self.dry_mode = int(os.getenv("DRY_MODE", "0"))
        self.time_to_sleep = int(os.getenv("TIME_TO_SLEEP", "10"))
        self.api = API("", self.api_key, 0, 0)
        self.CITY = City(self.api, self.detector_id).return_city()
        self.model = (
            YOLO("weight.pt")
            if not os.getenv("DISABLE_YOLO", "FALSE") == "true"
            else None
        )
        self.debug = True if os.getenv("DEBUG", "FALSE") == "true" else False
        self.run()

    def verif_time_one_hour(self) -> bool:
        if time.time() - self.time_for_one_hour > self.one_hour:
            self.time_for_one_hour = time.time()
            return True
        return False

    def predict_picture(self, frame):
        results = self.model.track(frame, persist=True)
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
                    print(
                        f"Erreur lors du traitement \
                          de l'image pour {self.city}: {e}"
                    )

    def set_value_for_city(self, index):
        if self.debug:
            print(self.CITY[index])
        self.city = self.CITY[index][0]
        self.latitude = self.CITY[index][1]
        self.longitude = self.CITY[index][2]
        self.ip = self.CITY[index][3]
        self.user_name = self.CITY[index][4]
        self.password = self.CITY[index][5]
        self.run_blur = self.CITY[index][6]
        self.run_detection = self.CITY[index][7]
        self.type_detection = self.CITY[index][8]
        self.launch_detection = self.CITY[index][9]
        self.stop_detection = self.CITY[index][10]
        self.public_url = self.CITY[index][11]
        self.save_picture = True if self.CITY[index][12] == 1 else False

    def run(self):
        caps = []
        for city in self.CITY:
            if city[8] is not None:
                rtsp_url = city[8]
            elif city[11] is None:
                rtsp_url = f"rtsp://admin:{city[5]}@{city[3]}/h264Preview_01_sub"
            else:
                rtsp_url = city[11]

            if self.debug:
                print(f"Connecting to camera: {city[0]} at {rtsp_url}")
            cap = cv2.VideoCapture(rtsp_url)
            if not cap.isOpened():
                print(f"Erreur: {city[0]}.")
            else:
                caps.append((cap, city[0]))

        if not caps:
            print("Erreur: Aucune caméra")
            return

        while True:
            frames = []
            for cap, city_name in caps:
                ret, frame = cap.read()
                if not ret:
                    print(f"Erreur: Impossible de lire la caméra a {city_name}.")
                    continue
                frames.append((frame, city_name))

            for i in range(len(self.CITY)):
                self.time_start = time.time()
                self.set_value_for_city(i)

                if self.run_detection:
                    self.api = API(
                        self.city, self.api_key, self.latitude, self.longitude
                    )

                    for frame, city_name in frames:
                        if city_name == self.city:
                            if self.debug:
                                print(f"Processing frame for city: {self.city}")

                            Scraper(
                                self.city,
                                self.ip,
                                self.user_name,
                                self.password,
                                self.run_blur,
                            ).save_picture(frame, self.save_picture)

                            lines_data = self.api.get_all_zone()
                            result_by_line = []
                            for line in lines_data:
                                if self.debug:
                                    print(
                                        f"Processing line: {line} for city: {self.city}"
                                    )
                                if line[5] == "opencv":
                                    result_by_line.append(
                                        [
                                            line[0],
                                            Detector.predict_nb_swimmer_by_zone_with_opencv(
                                                frame,
                                                x1=line[1],
                                                x2=line[2],
                                                y1=line[3],
                                                y2=line[4],
                                                filter_size=line[7],
                                                threshold_luminosity=line[8],
                                                stop_threshold_luminosity=line[9],
                                            ),
                                        ]
                                    )
                                elif line[5] == "yolo":
                                    result_by_line.append(
                                        [
                                            line[0],
                                            Detector.predict_nb_swimmer_by_zone_with_yolo(
                                                frame,
                                                x1=line[1],
                                                x2=line[2],
                                                y1=line[3],
                                                y2=line[4],
                                            ),
                                        ]
                                    )
                                elif line[5] == "yolo-alert":
                                    self.predict_picture(frame)
                                    self.detector = Detector(
                                        self.actual_data_predict_picture
                                    )
                                    self.api.set_number_people(
                                        self.detector.get_nb_beach(),
                                        self.detector.get_nb_sea(),
                                    )
                                    cache_size = City(
                                        self.api, self.detector_id
                                    ).get_cache_size()
                                    self.alert = Alert(
                                        self.latitude,
                                        self.longitude,
                                        self.actual_data_predict_picture,
                                        self.api,
                                        self.city,
                                        cache_size,
                                    )
                                    self.alert.run()
                                else:
                                    print(f"Unknown detection method: {line[5]}")

                            for zone_id, data in result_by_line:
                                if self.debug:
                                    print(f"Zone ID: {zone_id}, Data: {data}")
                                self.api.post_data_by_zone(zone_id, data)

                            if os.getenv("SEND_PICTURE", "FALSE") == "true":
                                self.api.add_picture_alert_or_moment(
                                    FOLDER_PICTURE + self.city + ".png"
                                )
                            print(
                                f"City: {self.city} has run in :\
                                   {time.time() - self.time_start}"
                            )

                else:
                    if self.debug:
                        print(f"Skipping detection for city: {self.city}")

            if self.dry_mode == 1:
                if frame is not None:
                    cv2.imshow("Video", frame)
                else:
                    print("Pas d'image")

                if cv2.waitKey(1) & 0xFF == ord("a"):
                    break

            time.sleep(self.time_to_sleep)

        for cap, _ in caps:
            cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    Main()
