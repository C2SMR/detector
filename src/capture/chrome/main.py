import undetected_chromedriver as uc


class Navigation:
    def __init__(self, url: str):
        self.url: str = url
        self.option = uc.ChromeOptions()
        self.option.add_argument("--incognito")
        self.option.add_argument('--disable-popup-blocking')
        self.option.add_argument("--headless")
        self.driver = uc.Chrome(options=self.option)
        self.driver.get(self.url)

    def screen_shot(self) -> None:
        self.driver.save_screenshot('../../pictures/picture.jpg')

    def run(self) -> None:
        self.screen_shot()
