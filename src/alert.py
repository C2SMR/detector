from src.weather import Weather


class Alert:
    def __init__(self, latitude: float, longitude: float):
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.weather = Weather(self.latitude, self.longitude)
