from ultralytics import YOLO
import cv2
import threading

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

model = YOLO("sign_Board/best.pt")

# --------------------------------------------------
# GLOBAL VALUES
# --------------------------------------------------

latest_sign = "NO SIGN"
latest_warning = "SAFE"

# --------------------------------------------------
# CLASS NAMES
# --------------------------------------------------

class_names = [

    "Speed limit 20",
    "Speed limit 30",
    "Speed limit 50",
    "Speed limit 60",
    "Speed limit 70",
    "Speed limit 80",
    "End speed limit 80",
    "Speed limit 100",
    "Speed limit 120",
    "No passing",
    "No passing trucks",
    "Right of way",
    "Priority road",
    "Yield",
    "Stop",
    "No vehicles",
    "Trucks prohibited",
    "No entry",
    "Danger",
    "Curve left",
    "Curve right",
    "Double curve",
    "Bumpy road",
    "Slippery road",
    "Road narrows",
    "Road work",
    "Traffic signals",
    "Pedestrian crossing",
    "Children crossing",
    "Bicycle crossing",
    "Snow",
    "Animals crossing",
    "End restrictions",
    "Turn right",
    "Turn left",
    "Go straight",
    "Go straight or right",
    "Go straight or left",
    "Keep right",
    "Keep left",
    "Roundabout",
    "End no passing"

]

# --------------------------------------------------
# CAMERA LOOP
# --------------------------------------------------

def camera_loop():

    global latest_sign
    global latest_warning

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        latest_sign = "NO CAMERA"
        latest_warning = "SAFE"

        return

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        # --------------------------------------------------
        # YOLO DETECTION
        # --------------------------------------------------

        results = model(
            frame,
            conf=0.90
        )

        boxes = results[0].boxes

        detected = False

        # --------------------------------------------------
        # PROCESS DETECTIONS
        # --------------------------------------------------

        for box in boxes:

            conf = float(box.conf[0])

            # EXTRA SAFETY FILTER
            if conf < 0.90:
                continue

            detected = True

            cls_id = int(box.cls[0])

            class_name = class_names[cls_id]

            latest_sign = class_name.upper()

            name = class_name.lower()

            # --------------------------------------------------
            # WARNING LOGIC
            # --------------------------------------------------

            if "stop" in name:

                latest_warning = "STOP VEHICLE"

            elif "yield" in name:

                latest_warning = "GIVE WAY"

            elif "speed limit" in name:

                latest_warning = class_name.upper()

            elif "pedestrian" in name:

                latest_warning = "PEDESTRIAN CROSSING"

            elif "children" in name:

                latest_warning = "CHILDREN CROSSING"

            elif "traffic" in name:

                latest_warning = "TRAFFIC SIGNAL"

            elif "road work" in name:

                latest_warning = "ROAD WORK AHEAD"

            elif "danger" in name:

                latest_warning = "DANGER"

            elif "no entry" in name:

                latest_warning = "NO ENTRY"

            else:

                latest_warning = "DRIVE CAREFULLY"

            # DRAW BOX

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0,255,0),
                2
            )

            label = f"{class_name} {conf:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
                2
            )

            break

        # --------------------------------------------------
        # NO DETECTION
        # --------------------------------------------------

        if not detected:

            latest_sign = "NO SIGN"
            latest_warning = "SAFE"

        # --------------------------------------------------
        # SHOW CAMERA WINDOW
        # --------------------------------------------------

        cv2.imshow(
            "AI Detection",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()

# --------------------------------------------------
# START CAMERA THREAD
# --------------------------------------------------

threading.Thread(
    target=camera_loop,
    daemon=True
).start()

# --------------------------------------------------
# RETURN DETECTION RESULT
# --------------------------------------------------

def get_detection():

    return latest_sign, latest_warning