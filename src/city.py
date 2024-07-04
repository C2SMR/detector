from api import API

class City:
    api: API
    detector_id: int

    def __init__(self, api: API, detector_id: int):
        self.api = api
        self.detector_id = detector_id

    def get_cache_size(self) -> int:
        return self.api.get_cache_size(self.detector_id)

    def return_city(self) -> list:
        return self.api.get_city_data(self.detector_id)
