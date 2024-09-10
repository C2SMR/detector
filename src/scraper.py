import cv2


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

    def get_picture(self, frame):
        cv2.imwrite(f"{self.folder_picture}/{self.city}.png", frame)
        if self.run_blur:
            self.apply_blur_on_picture()
        else:
            print("blur enable")

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
