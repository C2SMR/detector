class Detector:
    def __init__(self, data_picture: object):
        self.data_picture: object = data_picture

    def count_class(self, name_class: str):
        count: int = 0
        for data in self.data_picture["predictions"]:
            if data["class"] == name_class:
                count += 1
        return count

    def get_nb_beach(self) -> int:
        return self.count_class("person")

    def get_nb_sea(self) -> int:
        return self.count_class("person_in_water")

    def get_visibility(self) -> int:
        width_sea = self.data_picture["predictions"]["sea"]["width"]
        height_sea = self.data_picture["predictions"]["sea"]["width"]
        width_picture = self.data_picture["image"]["width"]
        height_picture = self.data_picture["image"]["width"]
        return int(width_sea*height_sea / width_picture*height_picture)
