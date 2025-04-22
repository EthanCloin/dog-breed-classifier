from flask import Flask, request, render_template, Response, jsonify
from werkzeug.datastructures import FileStorage
from uuid import uuid4
from pathlib import Path
import json
import logging

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent   # up three: app.py → app → backend → project root
# 2. An absolute path to templates/
TEMPLATES = PROJECT_ROOT / "frontend/templates"
# 2. An absolute path to uploads/
UPLOAD_PATH    = PROJECT_ROOT / "frontend/uploads"


app = Flask(__name__, template_folder=str(TEMPLATES))
app.config["UPLOAD_FOLDER"] = str(UPLOAD_PATH)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/") 
def index():
    return render_template("upload-pet.html")


@app.post("/new-pet")
def process_new_pet():
    try:
        image_id = uuid4()
        upload_path = Path(app.config["UPLOAD_FOLDER"])
        image: FileStorage = request.files.get("pet-image")

        extension = image.filename.split(".")[1]
        unique_filename = f"{image_id}.{extension}"
        logger.info("Saving file %s to %s", unique_filename, upload_path)
        image.save(upload_path / unique_filename)

        # TODO: tell the model to process the new image
        # TODO: return the updated webpage to await result.
        return Response(
            json.dumps({"status": "success", "data": {"id": str(image_id)}}),
            status=202,
            content_type="application/json",
        )
    except Exception as e:
        logger.exception("problem with upload", e)
        return Response(
            json.dumps(
                {"status": "error", "message": "unable to process image upload"}
            ),
            status=500,
        )


if __name__ == "__main__":
    app.run("0.0.0.0", 80, debug=True)
