from typing import List

import cv2
import numpy as np
from ultralytics import YOLO


class Detector:
    data_picture: object

    def __init__(self, data_picture: object):
        self.data_picture = data_picture

    def count_class(self, name_class: str) -> int:
        count: int = 0
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
                if data["class"] == name_class:
                    count += 1
        return count

    def get_nb_beach(self) -> int:
        return self.count_class("person")

    def get_nb_sea(self) -> int:
        return self.count_class("person_in_water")

    def get_visibility(self) -> int:
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
                if data["class"] == "sea":
                    width_sea = data["width"]
                    height_sea = data["height"]
                    width_picture = prediction["image"]["width"]
                    height_picture = prediction["image"]["height"]
                    return int(
                        width_sea * height_sea / (width_picture * height_picture)
                    )
        return -1

    def get_nb_boat(self) -> int:
        return (
            self.count_class("boat")
            + self.count_class("fishing_boat")
            + self.count_class("small_speedboat")
            + self.count_class("yacht")
        )

    @staticmethod
    def predict_nb_swimmer_by_zone_with_opencv(
        frame: np.ndarray,
        x1,
        x2,
        y1,
        y2,
        filter_size=1000,
        threshold_luminosity=60,
        stop_threshold_luminosity=100,
    ) -> int:
        x1, x2, y1, y2 = x1 / 10, x2 / 10, y1 / 10, y2 / 10
        width_picture = frame.shape[1]
        height_picture = frame.shape[0]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        luminosity = cv2.mean(gray)[0]
        _, filter = cv2.threshold(gray, threshold_luminosity, 255, cv2.THRESH_BINARY)
        filter = cv2.bitwise_not(filter)
        contours, _ = cv2.findContours(
            filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = [c for c in contours if cv2.contourArea(c) < filter_size]
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        nb_detection = 0
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if (
                x1 * width_picture < x < x2 * width_picture
                and y1 * height_picture < y < y2 * height_picture
            ):
                nb_detection += 1
        cv2.rectangle(
            frame,
            (int(x1 * width_picture), int(y1 * height_picture)),
            (int(x2 * width_picture), int(y2 * height_picture)),
            (255, 0, 0),
            2,
        )
        cv2.imwrite(f"debu{x1}_{x2}_{y1}_{y2}.png", frame)

        if luminosity < stop_threshold_luminosity:
            return -1
        return nb_detection

    @staticmethod
    def predict_nb_swimmer_by_zone_with_yolo(frame, x1, x2, y1, y2) -> int:
        model = YOLO("best.pt")
        results = model.predict(source=frame, save=False)
        nb_detection = 0
        for result in results:
            for box in result.boxes:
                x, y, w, h = box.xywh[0]
                if x1 < x < x2 and y1 < y < y2:
                    nb_detection += 1
        return nb_detection
