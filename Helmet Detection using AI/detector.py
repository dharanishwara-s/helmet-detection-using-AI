import cv2
from ultralytics import YOLO
import cvzone

# Load model
model = YOLO("best.pt")

with open("coco1.txt", "r") as f:
    class_list = f.read().splitlines()

HELMET_CONFIDENCE = 0.55   # 🔥 Increase for accuracy

def detect(img):
    helmet_count = 0

    results = model(
        img,
        conf=HELMET_CONFIDENCE,
        stream=True
    )

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = class_list[cls].lower()

            if label != "helmet":
                continue

            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            helmet_count += 1

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cvzone.putTextRect(
                img,
                f"Helmet {conf:.2f}",
                (x1, y1),
                scale=1,
                thickness=1,
                colorR=(0, 255, 0)
            )

    violation = "NO HELMET" if helmet_count == 0 else "HELMET OK"
    return img, helmet_count, violation
