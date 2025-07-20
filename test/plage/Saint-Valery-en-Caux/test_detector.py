import os

import cv2
from ultralytics import YOLO


class Main:
    def __init__(self):
        self.image_directory = "test/plage/Saint-Valery-en-Caux/"

    def run_yolo(self):
        m = YOLO("best.pt")
        for image in os.listdir(self.image_directory):
            if not image.endswith((".jpg", ".jpeg", ".png")):
                continue
            results = m.predict(
                source=os.path.join(self.image_directory, image), save=True
            )
            results[0].save(filename=f"test/plage/Saint-Valery-en-Caux/result_{image}")

    def run_opencv(self):
        for image in os.listdir(self.image_directory):
            if not image.endswith((".jpg", ".jpeg", ".png")):
                continue
            image_path = os.path.join(self.image_directory, image)
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            luminosity = cv2.mean(gray)[0]
            print(f"Image: {image}, Luminosity: {luminosity:.2f}")
            _, filter = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
            filter = cv2.bitwise_not(filter)
            contours, _ = cv2.findContours(
                filter, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            contours = [c for c in contours if cv2.contourArea(c) < 1000]
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            img = cv2.resize(img, (800, 600))
            cv2.imwrite(f"test/plage/Saint-Valery-en-Caux/result_{image}", img)


if __name__ == "__main__":
    # Main().run_yolo()
    Main().run_opencv()
