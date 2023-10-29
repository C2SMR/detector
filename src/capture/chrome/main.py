import undetected_chromedriver as uc
import time


class Navigation:
    def __init__(self, url: str):
        self.url: str = url
        self.option = uc.ChromeOptions()
        self.option.add_argument("--incognito")
        self.option.add_argument('--disable-popup-blocking')
        self.option.add_argument("--headless")
        self.option.add_argument('--disable-dev-shm-usage')
        self.option.add_argument('--no-sandbox')
        self.driver = uc.Chrome(options=self.option)
        self.driver.get(self.url)
        self.accept_cookie()
        self.full_screen()

    def accept_cookie(self):
        self.driver.execute_script(
            'document.cookie = "SOCS=CAESEwgDEgk1NzY'
            '3NTAwMzcaAmZyIAEaBgiAwfapBg"')
        self.driver.execute_script('document.location.reload()')

    def full_screen(self):
        time.sleep(2)
        self.driver.execute_script(
            "document.querySelector('.ytp-fullscreen-button')"
            ".click()")

    def screen_shot(self) -> None:
        self.driver.save_screenshot('pictures/picture.png')

    def run(self) -> None:
        self.screen_shot()
