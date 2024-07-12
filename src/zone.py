from api import API


class Zone:
    city: str
    api: API

    def __init__(self, city: str, api: API):
        self.city = city
        self.api = api

    def get_zone_orange(self):
        return self.api.get_zone_orange()

    def get_zone_red(self):
        return self.api.get_zone_red()

    def get_zone_green(self):
        return self.api.get_zone_green()
