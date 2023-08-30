from roboflow import Roboflow
import cv2

from src.config import PROJECT_WORKSPACE_ROBOFLOW, API_KEY_ROBOFLOW, TITLE


class Main:

    def __init__(self):
        self.rf = Roboflow(api_key=API_KEY_ROBOFLOW)
        self.project = self.rf.workspace().project(PROJECT_WORKSPACE_ROBOFLOW)
        self.model = self.project.version(2).model
        self.video = cv2.VideoCapture(0)

    def run(self):
        while True:
            cv2.imshow(TITLE, self.video.read()[1])
            if cv2.waitKey(1) == ord('q'):
                break
        self.video.release()
        cv2.destroyAllWindows()
