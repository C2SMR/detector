import cv2


class Scraper:
    def __init__(self, city: str, ip: str, user_name: str, password: str):
        self.video = None
        self.city: str = city
        self.ip: str = ip
        self.user_name: str = user_name
        self.password: str = password
        self.folder_picture: str = 'picture/'

    def get_picture(self):
        self.video = cv2.VideoCapture(f'rtsp://{self.user_name}:'
                                      f'{self.password}@{self.ip}'
                                      f'/h264Preview_01_sub')
        _, frame = self.video.read()

        cv2.imwrite(f'{self.folder_picture}/{self.city}.png', frame)
        self.apply_blur_on_picture()  # can be commented

    def apply_blur_on_picture(self):
        img = cv2.imread(f'{self.folder_picture}/{self.city}.png')
        face_cascade = cv2.CascadeClassifier('../haarcascade_'
                                             'frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.1, 4)
        for (x, y, w, h) in faces:
            img[y:y + h, x:x + w] = cv2.blur(img[y:y + h, x:x + w], (23, 23))
        cv2.imwrite(f'{self.folder_picture}/{self.city}.png', img)
