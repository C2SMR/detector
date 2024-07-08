import requests
import base64
from weather import Weather


class API:
    url: str
    city: str
    weather: Weather
    RASPBERRY_KEY: str

    def __init__(self, city: str, ras_key: str,
                 latitude: float, longitude: float):
        self.url = "https://api.c2smr.fr/machine"
        self.city = city
        self.weather = Weather(latitude, longitude)
        self.RASPBERRY_KEY = ras_key

    def set_flag(self, color: int):
        try:
            requests.post(self.url + "/set_flag", json={
                "key": self.RASPBERRY_KEY,
                "color": color,
                "city": self.city
            })
            print("change flag :)")
        except Exception as e:
            print(e)

    def set_number_people(self, nb_beach: int, nb_sea: int):
        requests.post(self.url + "/set_number_people", json={
            "key": self.RASPBERRY_KEY,
            "nb_beach": nb_beach,
            "nb_sea": nb_sea,
            "city": self.city
        })

    def delete_alert_by_city(self):
        requests.post(self.url + "/delete_alert_by_city", json={
            "key": self.RASPBERRY_KEY,
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
                "key": self.RASPBERRY_KEY,
                "color": color,
                "message": message,
                "city": self.city
            })
            print(f'send alert type {color} : {message}')
        except Exception as e:
            print(f"error : {e}")

    def add_data_city(self, nb_beach: int, nb_sea: int, cam_visibility: int):
        requests.post(self.url + "/add_data_city", json={
            "key": self.RASPBERRY_KEY,
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
            "key": self.RASPBERRY_KEY,
        }, files={
            'file': open(path_file, 'rb')
        })

    def get_picture(self):
        picture_base_64 = requests.post("https://api.c2smr.fr/"
                                        "client/get_picture",
                                        json={
                                            "city": self.city +
                                            '-not-trained'
                                            '.png'
                                        })
        picture_base_64 = picture_base_64.json()['picture']
        imgdata = base64.b64decode(picture_base_64)
        with open('picture/' + self.city + '.png', "wb") as f:
            f.write(imgdata)

    def get_city_data(self, detector_id: int):
        response = requests.get(f"{self.url}/city",
                                params={
                                    "detector_id": detector_id
                                    })
        response.raise_for_status()
        return response.json().get("data", [])

    def get_cache_size(self, detector_id: int):
        response = requests.get(f"{self.url}/cache_size",
                                params={
                                    "detector_id": detector_id
                                    })
        response.raise_for_status()
        return response.json().get("cache_size", 4)

    def get_zone_orange(self):
        response = requests.get(f"{self.url}/zone_orange",
                                params={
                                    "city": self.city
                                    })
        response.raise_for_status()
        return response.json().get("data", [])

    def get_zone_red(self):
        response = requests.get(f"{self.url}/zone_red",
                                params={
                                    "city": self.city
                                    })
        response.raise_for_status()
        return response.json().get("data", [])

    def get_zone_green(self):
        response = requests.get(f"{self.url}/zone_green",
                                params={
                                    "city": self.city
                                    })
        response.raise_for_status()
        return response.json().get("data", [])
