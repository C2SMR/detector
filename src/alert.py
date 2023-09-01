from src.weather import Weather


class Alert:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.weather = Weather(self.latitude, self.longitude)
