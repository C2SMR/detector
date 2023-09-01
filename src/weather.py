import requests
import json
from datetime import datetime


class Weather:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.data = {}
        self.api_url = "https://api.open-meteo.com/v1/meteofrance?" \
                       "latitude=" + self.latitude + \
                       "&longitude=" + self.longitude + \
                       "&hourly=temperature_2m," \
                       "precipitation," \
                       "cloudcover,cloudcover_low," \
                       "windspeed_10m"

    def fetch_data(self):
        res = requests.get(self.api_url)
        self.data = json.loads(res.text)

    def template_get_data(self, name_data):
        lst_total = self.data["hourly"][name_data]
        lst_to_return = []
        now = int(datetime.now().strftime('%H'))
        for i in range(now, now + 8):
            lst_to_return.append(lst_total[i])
        return lst_to_return

    def get_precipitation(self):
        return self.template_get_data("precipitation")

    def get_cloud_cover(self):
        return self.template_get_data("cloudcover")

    def get_wind_speed(self):
        return self.template_get_data("windspeed_10m")

    def get_temperature_(self):
        return self.template_get_data("temperature_2m")

    def get_visibility(self):
        return self.template_get_data("cloudcover_low")
