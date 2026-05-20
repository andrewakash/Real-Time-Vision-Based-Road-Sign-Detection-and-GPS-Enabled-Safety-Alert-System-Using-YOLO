from ultralytics import YOLO
import cv2

# -------------------------------
# LOAD MODEL
# -------------------------------
model = YOLO("sign_Board/best.pt")

# -------------------------------
# FIX CLASS NAMES (GTSRB 42)
# -------------------------------
class_names = [
"Speed limit 20", "Speed limit 30", "Speed limit 50", "Speed limit 60",
"Speed limit 70", "Speed limit 80", "End speed limit 80", "Speed limit 100",
"Speed limit 120", "No passing", "No passing trucks",
"Right of way", "Priority road", "Yield", "Stop",
"No vehicles", "Trucks prohibited", "No entry",
"Danger", "Curve left", "Curve right", "Double curve",
"Bumpy road", "Slippery road", "Road narrows",
"Road work", "Traffic signals", "Pedestrian crossing",
"Children crossing", "Bicycle crossing",
"Snow", "Animals crossing",
"End restrictions", "Turn right", "Turn left",
"Go straight", "Go straight or right", "Go straight or left",
"Keep right", "Keep left", "Roundabout", "End no passing"
]

# -------------------------------
# WARNING LOGIC
# -------------------------------
def get_warning(class_name):   # ✅ correct parameter

    name = class_name.lower()

    if "stop" in name:
        return "🚫 STOP VEHICLE"

    elif "yield" in name:
        return "⚠ Give Way"

    elif "speed limit" in name:
        return f"⚠ {class_name}"

    elif "no entry" in name:
        return "🚫 No Entry"

    elif "road work" in name:
        return "⚠ Road Work Ahead"

    elif "pedestrian" in name:
        return "⚠ Pedestrian Crossing"

    elif "children" in name:
        return "⚠ Children Crossing"

    elif "traffic signal" in name:
        return "🚦 Traffic Signal Ahead"

    else:
        return ""

# -------------------------------
# CAMERA START
# -------------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not working")
    exit()

print("✅ Camera started... Press Q to exit")

# -------------------------------
# MAIN LOOP
# -------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, conf=0.25)
    boxes = results[0].boxes

    for box in boxes:

        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        # ✅ USE YOUR CLASS LIST
        class_name = class_names[cls_id]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)

        label = f"{class_name} {conf:.2f}"
        cv2.putText(frame, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # warning
        warning = get_warning(class_name)

        if warning:
            cv2.putText(frame, warning, (50,50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,0,255), 3)

            print("⚠ ALERT:", warning)

    cv2.imshow("Traffic Sign Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()