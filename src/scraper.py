import os

import cv2
from datetime import datetime


class Scraper:
    video: cv2.VideoCapture
    city: str
    ip: str
    user_name: str
    password: str
    folder_picture: str
    run_blur: bool

    def __init__(
        self, city: str, ip: str, user_name: str, password: str, run_blur: bool
    ):
        self.city = city
        self.ip = ip
        self.user_name = user_name
        self.password = password
        self.folder_picture = "picture/"
        self.run_blur = run_blur
        self.debug = os.getenv("DEBUG", "False") == "true"

    def save_picture(self, frame, save: bool = True) -> None:
        if not save:
            cv2.imwrite(f"{self.folder_picture}/{self.city}.png", frame)
        else:
            now = datetime.now()
            if not os.path.exists(f"{self.folder_picture}/{self.city}"):
                os.makedirs(f"{self.folder_picture}/{self.city}")
            cv2.imwrite(
                f"{self.folder_picture}/{self.city}/{now.strftime('%Y-%m-%d_%H-%M-%S')}.png",
                frame,
            )
            if self.debug:
                print(f"Picture saved in {self.folder_picture} folder for {self.city}")
        if self.run_blur:
            self.apply_blur_on_picture()
        else:
            if self.debug:
                print("blur disabled, not apply")

    def apply_blur_on_picture(self):
        img = cv2.imread(f"{self.folder_picture}/{self.city}.png")
        face_cascade = cv2.CascadeClassifier(
            "../haarcascade_" "frontalface_default.xml"
        )
        faces = face_cascade.detectMultiScale(img, 1.1, 4)
        for x, y, w, h in faces:
            img[y : y + h, x : x + w] = cv2.blur(img[y : y + h, x : x + w], (23, 23))
        cv2.imwrite(f"{self.folder_picture}/{self.city}.png", img)
        print("blur apply")
