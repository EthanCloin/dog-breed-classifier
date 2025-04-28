from ultralytics import YOLO

# Load the trained/best weights
model_path = r"C:\Users\johnb\Downloads\Masters\ML\f_project\adoption-blurb-generator\backend\models\dog_detection\best.pt"
model = YOLO(model_path)

IMAGE_PATH = r"C:\Users\johnb\Downloads\fluffy.jpeg"
# 2) Run inference
results = model.predict(
    source=IMAGE_PATH,
    imgsz=640,      # match your training size
    conf=0.25,      # confidence threshold
    iou=0.45,       # NMS IoU threshold
    save=False,     # we'll handle saving manually
    verbose=False
)

# Get the first (and only) Results object
result = results[0]

# Get bounding boxes (x1, y1, x2, y2 format)
boxes = result.boxes.xyxy.cpu().numpy()

# Get confidence scores
confidences = result.boxes.conf.cpu().numpy()

# Get class IDs
class_ids = result.boxes.cls.cpu().numpy().astype(int)

# Get class names dictionary
class_names = result.names

# Print the first detection as an example
if len(boxes) > 0:
    print(f"First detection:")
    print(f"- Box: {boxes[0]}")
    print(f"- Confidence: {confidences[0]:.2f}")
    print(f"- Class ID: {class_ids[0]}")
    print(f"- Class name: {class_names[class_ids[0]]}")