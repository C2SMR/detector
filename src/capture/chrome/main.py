import random
import sys
import time

import undetected_chromedriver as webdriver
from config import FOLDER_PICTURE, NAME_PICTURE


def full_screen():
    time.sleep(2)


class Navigation:
    def __init__(self):
        self.driver = None

        self.lst_article = None
        self.url: str = sys.argv[1]
        self.dir = "dataset"
        location: str = "C:/Program Files\
                        Google/Chrome Beta\
                        Application/chrome.exe"
        self.option: object = webdriver.ChromeOptions()
        self.option.binary_location = location
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get(self.url)
        full_screen()
        self.run()
        self.driver.close()

    def screen_shot(self):
        self.driver.save_screenshot('../..' + FOLDER_PICTURE + NAME_PICTURE)

    def run(self):
        time.sleep(2)
        while True:
            time.sleep(random.randint(0, 10))

            self.screen_shot()


Navigation()
