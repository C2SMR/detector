from roboflow import Roboflow
import sys
import cv2


class Main:

    def __init__(self):
        self.actual_data_predict_picture = None
        self.rf = Roboflow(api_key="rBzJE5DXKnwjcrNDnOxw")
        self.project = self.rf.workspace().project("c2smr")
        self.model = self.project.version(4).model
        self.run()

    def run(self):
        detection = self.model.predict(sys.argv[1]).json()

        image = cv2.imread(sys.argv[1])

        for data in detection["predictions"]:
            x = data["x"]
            y = data["y"]
            w = data["width"]
            h = data["height"]
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, data["class"], (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        while True:
            image = cv2.resize(image, (800, 600))
            cv2.imshow("image", image)
            if cv2.waitKey(30) == 27:
                break


if __name__ == '__main__':
    Main()
