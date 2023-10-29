import requests
import json
from datetime import datetime


class Weather:
    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.data: object = {}
        self.api_url: str = "https://api.open-meteo.com/v1/meteofrance?" \
                            "latitude=" + str(self.latitude) + \
                            "&longitude=" + str(self.longitude) + \
                            "&hourly=temperature_2m," \
                            "precipitation," \
                            "cloudcover,cloudcover_low," \
                            "windspeed_10m"
        self.fetch_data()

    def fetch_data(self):
        res = requests.get(self.api_url)
        self.data = json.loads(res.text)

    def template_get_data(self, name_data: str) -> float:
        lst: list = self.data["hourly"][name_data]
        now: int = int(datetime.now().strftime('%H'))
        return lst[now]

    def get_precipitation(self) -> float:
        return self.template_get_data("precipitation")

    def get_cloud_cover(self) -> float:
        return self.template_get_data("cloudcover")

    def get_wind_speed(self) -> float:
        return self.template_get_data("windspeed_10m")

    def get_temperature(self) -> float:
        return self.template_get_data("temperature_2m")

    def get_visibility(self) -> float:
        return self.template_get_data("cloudcover_low")
