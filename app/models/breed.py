
import os
# suppress INFO and WARNING logs (0 = all, 1 = filter out INFO, 2 = filter out INFO+WARNING, 3 = filter out all but ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# # disable oneDNN custom ops if you really want to silence that specific message
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]


CLASS_NAME_JSON = PROJECT_ROOT / "backend"  / "models"   / "dog_breed_model" / "class_names.json"
MODEL_LOCATION  = PROJECT_ROOT / "backend"  / "models"   / "dog_breed_model" / "best_model.h5"
IMG_PATH        = PROJECT_ROOT / "frontend" / "uploads" / "cd8fa84f-ecc7-4f86-9c3a-e74fe9e5a40f.jpeg"  # or your actual filename


if not CLASS_NAME_JSON.is_file():
    print(f"ERROR: class_names.json not found at {CLASS_NAME_JSON}", file=sys.stderr)
    sys.exit(1)

if not MODEL_LOCATION.is_file():
    print(f"ERROR: model not found at {MODEL_LOCATION}", file=sys.stderr)
    sys.exit(1)

if not IMG_PATH.is_file():
    print(f"ERROR: image not found at {IMG_PATH}", file=sys.stderr)
    sys.exit(1)

# Load the class↔index mapping 
with open(CLASS_NAME_JSON, "r") as f:
    class_map = json.load(f)

# invert if needed: assume JSON is {"breed_name": index, ...}
if all(isinstance(v, int) for v in class_map.values()):
    idx_to_class = {v: k for k, v in class_map.items()}
else:
    # or if JSON is {"0":"breed_name", ...}
    idx_to_class = {int(k): v for k, v in class_map.items()}

# Load your trained model (no compile, inference only) 
model = load_model(str(MODEL_LOCATION), compile=False)

#  Preprocess your input image 
IMG_SIZE = (299, 299)
img = image.load_img(str(IMG_PATH), target_size=IMG_SIZE)
x   = image.img_to_array(img) / 255.0
x   = np.expand_dims(x, axis=0)  # shape → (1, 299, 299, 3)

#  Predict
preds      = model.predict(x)
pred_idx   = int(np.argmax(preds[0]))
pred_prob  = float(preds[0][pred_idx])
pred_breed = idx_to_class.get(pred_idx, "UNKNOWN")

print(f"Predicted breed: {pred_breed}")
print(f"Confidence: {pred_prob*100:.1f}%")
