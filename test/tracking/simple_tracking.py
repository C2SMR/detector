import cv2
from ultralytics import YOLO
import sys


def main():
    cap = cv2.VideoCapture(sys.argv[1])

    model = YOLO(sys.argv[2])

    while True:
        ret, frame = cap.read()
        results = model.track(frame, persist=True)
        res_plotted = results[0].plot()
        cv2.imshow("frame", res_plotted)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
