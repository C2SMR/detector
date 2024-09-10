class Detector:
    data_picture: object

    def __init__(self, data_picture: object):
        self.data_picture = data_picture

    def count_class(self, name_class: str) -> int:
        count: int = 0
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
                if data["class"] == name_class:
                    count += 1
        return count

    def get_nb_beach(self) -> int:
        return self.count_class("person")

    def get_nb_sea(self) -> int:
        return self.count_class("person_in_water")

    def get_visibility(self) -> int:
        for prediction in self.data_picture:
            for data in prediction.get("predictions", []):
                if data["class"] == "sea":
                    width_sea = data["width"]
                    height_sea = data["height"]
                    width_picture = prediction["image"]["width"]
                    height_picture = prediction["image"]["height"]
                    return int(
                        width_sea * height_sea / (width_picture * height_picture)
                    )
        return -1

    def get_nb_boat(self) -> int:
        return (
            self.count_class("boat")
            + self.count_class("fishing_boat")
            + self.count_class("small_speedboat")
            + self.count_class("yacht")
        )
