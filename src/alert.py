from api import API
from zone import Zone
from weather import Weather
from detector import Detector

ALERT_CACHE_SIZE = 4


class Alert:
    number_alerts: int
    city: str
    latitude: float
    longitude: float
    data_picture: object
    api: API
    weather: Weather
    detector: Detector
    zone: Zone
    alert_cache: list

    def __init__(
        self,
        latitude: float,
        longitude: float,
        data_picture: object,
        api: API,
        city: str,
        cache_size: int,
    ):
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.data_picture = data_picture
        self.api = api
        self.weather = Weather(self.latitude, self.longitude)
        self.detector = Detector(self.data_picture)
        self.api.delete_alert_by_city()
        self.zone = Zone(self.city, self.api)
        self.alert_cache = []
        self.cache_size = cache_size
        self.run()

    def add_to_cache(self, alert_type: int, alert_message: str) -> None:
        self.alert_cache.append((alert_type, alert_message))
        if len(self.alert_cache) >= self.cache_size:
            self.send_alerts()

    def send_alerts(self) -> None:
        for alert_type, alert_message in self.alert_cache:
            self.api.add_alert(alert_type, alert_message)
        self.alert_cache = []

    def run(self) -> None:
        self.number_alerts = 0
        self.no_one()
        self.beach_full()
        self.have_boat()
        self.rain()
        self.hard_wind()
        self.swimmer_away()
        self.hot()
        self.no_sea_detected()
        self.change_flag()
        self.swimmer_in_danger_zone()
        self.swimmer_in_danger_zone_if_sea_is_not_detected()
        self.boat_is_near_to_swimmer()

    @staticmethod
    def distance_swimmer(swimmer: object) -> int:
        width_swimmer = swimmer["width"]
        know_width = 34
        know_dist = 20
        focal_length = know_dist * width_swimmer / know_width
        distance = focal_length * know_dist / width_swimmer
        return distance

    def no_one(self) -> None:
        if self.detector.get_nb_beach() + self.detector.get_nb_sea() == 0:
            self.number_alerts += 1
            self.add_to_cache(1, "Plage vide.")

    def beach_full(self) -> None:
        if self.detector.get_nb_beach() + self.detector.get_nb_sea() > 100:
            self.number_alerts += 1
            self.add_to_cache(0, "Beaucoup de personnes sur la plage")

    def have_boat(self) -> None:
        if self.detector.get_nb_boat():
            self.number_alerts += 1
            self.add_to_cache(1, "Bateau dans l'eau")

    def boat_is_near_to_swimmer(self) -> None:
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
                if data["class"] in [
                    "boat",
                    "fishing_boat",
                    "small_speedboat",
                    "yatch",
                ]:
                    for data_swimmer in prediction.get("predictions", []):
                        if data_swimmer["class"] == "person_in_water":
                            if (
                                abs(data["x"] - data_swimmer["x"]) < 50
                                and abs(data["y"] - data_swimmer["y"]) < 50
                            ):
                                self.number_alerts += 1
                                self.add_to_cache(
                                    2, "Un bateau est proche d'une personne"
                                )

    def rain(self) -> None:
        if self.weather.get_precipitation() > 0.8:
            self.number_alerts += 1
            self.add_to_cache(1, "Pluie")

    def hard_wind(self) -> None:
        if self.weather.get_wind_speed() > 60:
            self.number_alerts += 1
            self.add_to_cache(2, "Vents violents")

    def swimmer_away(self) -> None:
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
                if data["class"] == "person_in_water":
                    if self.distance_swimmer(data) > 100:
                        self.number_alerts += 1
                        self.add_to_cache(1, "Une personne s'éloigne")

    def hot(self) -> None:
        if self.weather.get_temperature() > 35:
            self.number_alerts += 1
            self.add_to_cache(0, "Température très élevée")

    def no_sea_detected(self) -> None:
        if self.detector.get_nb_sea() == -1:
            self.number_alerts += 1
            self.add_to_cache(1, "Mer non détectée")

    def swimmer_in_danger_zone(self) -> None:
        danger_zone: list[list[int]] = self.zone.get_zone_red()
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
                if data["class"] == "person_in_water" or data["class"] == "swimmer":
                    for zone in danger_zone:
                        if (
                            zone[0] < data["x"] < zone[0] + zone[2]
                            and zone[1] < data["y"] < zone[1] + zone[3]
                        ):
                            self.number_alerts += 1
                            self.add_to_cache(
                                2, "Une personne est dans une zone dangereuse"
                            )

    def get_sea_dimensions(self) -> list[int]:
        for data in self.data_picture["predictions"]:
            if data["class"] == "sea":
                return [data["x"], data["y"], data["width"], data["height"]]

    def swimmer_in_danger_zone_if_sea_is_not_detected(self) -> None:
        danger_zone: list[list[int]] = self.zone.get_zone_orange()
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
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
                                and +zone[2] < sea_dimensions[0] + sea_dimensions[2]
                                and sea_dimensions[1]
                                < zone[1]
                                < sea_dimensions[1] + sea_dimensions[3]
                                and sea_dimensions[1]
                                < zone[1] + zone[3]
                                < sea_dimensions[1] + sea_dimensions[3]
                            ):
                                self.number_alerts += 1
                                self.add_to_cache(
                                    2,
                                    "Une personne est dans \
                                une zone dangereuse \
                                (Niveau de la mer faible)",
                                )

    def swimmer_in_long_zone(self) -> None:
        danger_zone: list[list[int]] = self.zone.get_zone_green()
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
                            self.add_to_cache(
                                2,
                                "Une personne est \
                                               dans une zone éloignée",
                            )

    def change_flag(self) -> None:
        if self.number_alerts < 4:
            self.api.set_flag(0)
        elif self.number_alerts < 10:
            self.api.set_flag(1)
        else:
            self.api.set_flag(2)
