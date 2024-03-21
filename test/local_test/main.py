import cv2
from ultralytics import YOLO


def main():
    cap = cv2.VideoCapture("./test.mp4")
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    model = YOLO("yolov8n.pt")

    while True:
        ret, frame = cap.read()
        results = model(frame, agnostic_nms=True)[0]

        if not results or len(results) == 0:
            continue

        for result in results:

            detection_count = result.boxes.shape[0]

            for i in range(detection_count):
                cls = int(result.boxes.cls[i].item())
                name = result.names[cls]
                confidence = float(result.boxes.conf[i].item())
                bounding_box = result.boxes.xyxy[i].cpu().numpy()
                text = f"{name}: {confidence:.2f}"

                x = int(bounding_box[0])
                y = int(bounding_box[1])
                width = int(bounding_box[2] - x)
                height = int(bounding_box[3] - y)
                cv2.putText(frame, text, (x, y - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + width, y + height),
                              (0, 255, 0), 2)
                cv2.imshow("frame", frame)

        if cv2.waitKey(30) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
