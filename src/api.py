import requests

from config import RASPBERRY_KEY
from weather import Weather


class API:
    def __init__(self, city: str):
        self.url: str = "https://api.c2smr.fr/machine"
        self.city: str = city
        self.weather: object = Weather

    def set_flag(self, color: int):
        try:
            requests.post(self.url + "/set_flag", json={
                "key": RASPBERRY_KEY,
                "color": color,
                "city": self.city
            })
            print("change flag :)")
        except Exception:
            print(Exception)

    def set_number_people(self, nb_beach: int, nb_sea: int):
        requests.post(self.url + "/set_number_people", json={
            "key": RASPBERRY_KEY,
            "nb_beach": nb_beach,
            "nb_sea": nb_sea,
            "city": self.city
        })

    def delete_alert_by_city(self):
        requests.post(self.url + "/delete_alert_by_city", json={
            "key": RASPBERRY_KEY,
            "city": self.city
        })
        self.add_alert(0, "Plage surveillée")

    def add_alert(self, color: int, message: str):
        """
        :param color: -> 0, 1, 2
        :param message:
        :return:
        """
        try:
            requests.post(self.url + "/add_alert", json={
                "key": RASPBERRY_KEY,
                "color": color,
                "message": message,
                "city": self.city
            })
            print("alert send :)")
        except Exception:
            print(f"error : {Exception}")

    def add_data_city(self, nb_beach: int, nb_sea: int, cam_visibility: int):
        requests.post(self.url + "/add_data_city", json={
            "key": RASPBERRY_KEY,
            "city": self.city,
            "nb_beach": nb_beach,
            "nb_sea": nb_sea,
            "precipitation": self.weather.get_precipitation(),
            "temp_beach": self.weather.get_temperature(),
            "cloud_cover": self.weather.get_cloud_cover(),
            "wind": self.weather.get_wind_speed(),
            "visibility": self.weather.get_visibility(),
            "cam_visibility": cam_visibility
        })

    def add_picture_alert_or_moment(self, path_file: str):
        requests.post(self.url + "/add_picture_alert_or_moment", json={
            "key": RASPBERRY_KEY,
        }, files={
            open(path_file, 'rb')
        })
