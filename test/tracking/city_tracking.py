import json
from typing import List

import cv2
from ultralytics import YOLO
import sys

from src.api import API


def main():
    cap = cv2.VideoCapture(sys.argv[1])

    model = YOLO(sys.argv[2])
    city: str = sys.argv[3]
    ras_key: str = sys.argv[4]
    zones: List[List[List[int]]] = []

    api = API(city, ras_key, 0, 0)
    if len(sys.argv) > 5:
        api.url = sys.argv[5]

    zones.append(api.get_zone_green())
    zones.append(api.get_zone_orange())
    zones.append(api.get_zone_red())

    for zone in zones:
        if zone:
            zone[0][1] -= 50

    while True:
        ret, frame = cap.read()

        if ret:
            results = model.track(frame, persist=True)

            results_json = json.loads(results[0].tojson())

            for res in results_json:
                x1 = res["box"]["x1"]
                y1 = res["box"]["y1"]
                x2 = res["box"]["x2"]
                y2 = res["box"]["y2"]
                x3 = res["box"]["x3"]
                y3 = res["box"]["y3"]
                x4 = res["box"]["x4"]
                y4 = res["box"]["y4"]
                cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.line(frame, (int(x2), int(y2)), (int(x3), int(y3)), (0, 255, 0), 2)
                cv2.line(frame, (int(x3), int(y3)), (int(x4), int(y4)), (0, 255, 0), 2)
                cv2.line(frame, (int(x4), int(y4)), (int(x1), int(y1)), (0, 255, 0), 2)
                for zone in zones:
                    if zone:
                        if (
                            zone[0][0] < x1 < zone[0][0] + zone[0][2]
                            and zone[0][1] < y1 < zone[0][1] + zone[0][3]
                        ):
                            cv2.putText(
                                frame,
                                "Alert",
                                (0, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                2,
                                (0, 0, 255),
                                2,
                            )

            for zone in zones:
                if zone:
                    cv2.rectangle(
                        frame,
                        (zone[0][0], zone[0][1]),
                        (zone[0][0] + zone[0][2], zone[0][1] + zone[0][3]),
                        (255, 0, 0),
                        2,
                    )

            cv2.imshow("frame", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
