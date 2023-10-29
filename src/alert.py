from api import API
from weather import Weather
from detector import Detector


def distance_swimmer(swimmer: object) -> int:
    width_swimmer = swimmer["width"]
    know_width = 34
    know_dist = 20  # en metre
    focal_length = know_dist * width_swimmer / know_width
    distance = focal_length * know_dist / width_swimmer
    return distance


class Alert:
    def __init__(self, latitude: float, longitude: float,
                 data_picture: object, api: API):
        self.number_alerts = None
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.data_picture: object = data_picture
        self.api: API = api
        self.weather: Weather = Weather(self.latitude, self.longitude)
        self.detector: Detector = Detector(self.data_picture)
        self.api.delete_alert_by_city()  # delete old alert picture
        self.run()

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

    def no_one(self) -> None:
        if self.detector.get_nb_beach() + self.detector.get_nb_sea() == 0:
            self.number_alerts += 1
            self.api.add_alert(1, "Plage vide.")

    def beach_full(self) -> None:
        if self.detector.get_nb_beach() + self.detector.get_nb_sea() > 100:
            self.number_alerts += 1
            self.api.add_alert(0, "Beacoup de personne sur la plage")

    def have_boat(self) -> None:
        if self.detector.get_nb_boat():
            self.number_alerts += 1
            self.api.add_alert(1, "Bateau dans l'eau")

    def rain(self) -> None:
        if self.weather.get_precipitation() > .8:
            self.number_alerts += 1
            self.api.add_alert(1, "Pluie")

    def hard_wind(self) -> None:
        if self.weather.get_wind_speed() > 60:
            self.number_alerts += 1
            self.api.add_alert(2, "Vent violents")

    def swimmer_away(self) -> None:
        for data in self.data_picture["predictions"]:
            if data["class"] == "person_in_water":
                if distance_swimmer(data) > 100:
                    self.number_alerts += 1
                    self.api.add_alert(1, "Une personne s'éloigne")

    def hot(self) -> None:
        if self.weather.get_temperature() > 35:
            self.number_alerts += 1
            self.api.add_alert(0, "Température très élevés")

    def no_sea_detected(self) -> None:
        if self.detector.get_nb_sea() == -1:
            self.number_alerts += 1
            self.api.add_alert(1, "Mer non détéctée")

    def change_flag(self):
        if self.number_alerts < 4:
            self.api.set_flag(0)
        elif self.number_alerts < 10:
            self.api.set_flag(1)
        else:
            self.api.set_flag(2)
