# C2SMR - DETECTOR


#### Detector for raspberry pi
#### Work in a serv for all city

---

## TECHNO

![](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

---

## LAUNCH

- Configure .env file

````shell
docker compose up --build
````

- Capture folder
  - chrome (for yt stream)
  - opencv (for cam)

## DEV

---

### ADD ALERT

---

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

---

### Add roboflow Project

---

- in main.py constructor
```python
    self.OTHER_PROJECT_ROBOFLOW: list = [
            Roboflow(api_key="key").workspace()
            .project("project_name")
            .version(project_version).model
        ]

```

### Add city : 

---

- in city.py
````python
CITY: list[list[str | float]] = [
    ["Villers-sur-mer", 49.3247, 0.0014,'ipadress:port','user_cam','password_cam']
]
````

## Train

---

```bash
cd train
py train.py api-key project-workspace project-name project-version nb-epoch nb-run
example : py train.py rBzJE5DXKnwjcrNDnOxw c2smr c2smr-villers 2 100 2
```

- if you are an error with the train step, rename data.yaml in your dataset to yolov8-obb.yaml
- if you are an error with the test, verify the path of train folder (the number)
- Get your best.pt