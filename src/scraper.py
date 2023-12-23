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
