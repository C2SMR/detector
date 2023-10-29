# C2SMR - DETECTOR

---

## TECHNO

![](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=OpenCV&logoColor=white)
![](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=Raspberry%20Pi&logoColor=white)

---

## LAUNCH

- Configure .env file

````shell
docker compose up --build
````

- Capture folder
  - chrome (for yt stream)
  - opencv (for cam)

## ADD ALERT

#### Go to alert.py
##### Add your new method in run() (and update the README)
````python
    def run(self) -> None:
        self.no_one()
        self.beach_full()
        self.have_boat()
        self.rain()
        self.hard_wind()
        self.swimmer_away()
        self.hot()
        self.no_sea_detected()
````