from detector import Detector
from object import zoneRed, zoneGreen, zoneOrange


class Alert:
    number_alerts: int
    data_picture: object
    detector: Detector

    def __init__(self, data_picture: object):
        self.data_picture = data_picture
        self.detector = Detector(self.data_picture)
        self.number_alerts = 0

    def get_number_alerts(self) -> int:
        return self.number_alerts

    def run(self) -> None:
        self.no_one()
        self.beach_full()
        self.have_boat()
        self.swimmer_away()
        self.no_sea_detected()
        self.swimmer_in_danger_zone()
        self.swimmer_in_danger_zone_if_sea_is_not_detected()
        self.boat_is_near_to_swimmer()

    @staticmethod
    def distance_swimmer(swimmer: object) -> int:
        width_swimmer = swimmer["width"]
        know_width = 34
        know_dist = 20  # en metre
        focal_length = know_dist * width_swimmer / know_width
        distance = focal_length * know_dist / width_swimmer
        return distance

    def no_one(self) -> None:
        if self.detector.get_nb_beach() + self.detector.get_nb_sea() == 0:
            self.number_alerts += 1

    def beach_full(self) -> None:
        if self.detector.get_nb_beach() + self.detector.get_nb_sea() > 100:
            self.number_alerts += 1

    def have_boat(self) -> None:
        if self.detector.get_nb_boat():
            self.number_alerts += 1

    def boat_is_near_to_swimmer(self) -> None:
        for data in self.data_picture["predictions"]:
            if data["class"] == "boat":
                for data_swimmer in self.data_picture["predictions"]:
                    if data_swimmer["class"] == "person_in_water":
                        if (
                            abs(data["x"] - data_swimmer["x"]) < 50
                            and abs(data["y"] - data_swimmer["y"]) < 50
                        ):
                            self.number_alerts += 1
                            print("boat is near to swimmer")

    def swimmer_away(self) -> None:
        for data in self.data_picture["predictions"]:
            if data["class"] == "person_in_water":
                if self.distance_swimmer(data) > 100:
                    self.number_alerts += 1
                    print("swimmer is away")

    def no_sea_detected(self) -> None:
        if self.detector.get_nb_sea() == -1:
            self.number_alerts += 1
            print("no sea detected")

    def swimmer_in_danger_zone(self) -> None:
        danger_zone: list[list[int]] = zoneRed
        for data in self.data_picture["predictions"]:
            if data["class"] == "person_in_water":
                for zone in danger_zone:
                    if (
                        zone[0] < data["x"] < zone[0] + zone[2]
                        and zone[1] < data["y"] < zone[1] + zone[3]
                    ):
                        self.number_alerts += 1
                        print("swimmer in danger zone")

    def get_sea_dimensions(self) -> list[int]:
        for data in self.data_picture["predictions"]:
            if data["class"] == "sea":
                return [data["x"], data["y"], data["width"], data["height"]]

    def swimmer_in_danger_zone_if_sea_is_not_detected(self) -> None:
        danger_zone: list[list[int]] = zoneOrange
        for data in self.data_picture["predictions"]:
            if data["class"] == "person_in_water":
                for zone in danger_zone:
                    if (
                        zone[0] < data["x"] < zone[0] + zone[2]
                        and zone[1] < data["y"] < zone[1] + zone[3]
                    ):
                        sea_dimensions = self.get_sea_dimensions()
                        if not (
                            sea_dimensions[0]
                            < zone[0]
                            < sea_dimensions[0] + sea_dimensions[2]
                            and sea_dimensions[0]
                            < zone[0] + zone[2]
                            < sea_dimensions[0] + sea_dimensions[2]
                            and sea_dimensions[1]
                            < zone[1]
                            < sea_dimensions[1] + sea_dimensions[3]
                            and sea_dimensions[1]
                            < zone[1] + zone[3]
                            < sea_dimensions[1] + sea_dimensions[3]
                        ):
                            self.number_alerts += 1
                            print(
                                "swimmer in danger zone if sea is not "
                                "completely detected"
                            )

    def swimmer_in_long_zone(self) -> None:
        danger_zone: list[list[int]] = zoneGreen
        for data in self.data_picture["predictions"]:
            if data["class"] == "person_in_water":
                for zone in danger_zone:
                    if (
                        zone[0] < data["x"] < zone[0] + zone[2]
                        and zone[1] < data["y"] < zone[1] + zone[3]
                    ):
                        sea_dimensions = self.get_sea_dimensions()
                        if (
                            sea_dimensions[0]
                            < zone[0]
                            < sea_dimensions[0] + sea_dimensions[2]
                            and sea_dimensions[0]
                            < zone[0] + zone[2]
                            < sea_dimensions[0] + sea_dimensions[2]
                            and sea_dimensions[1]
                            < zone[1]
                            < sea_dimensions[1] + sea_dimensions[3]
                            and sea_dimensions[1]
                            < zone[1] + zone[3]
                            < sea_dimensions[1] + sea_dimensions[3]
                        ):
                            self.number_alerts += 1
                            print("swimmer in long zone")
