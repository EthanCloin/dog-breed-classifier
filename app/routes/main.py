from flask import Blueprint, request, render_template, Response, current_app, g
from uuid import uuid4
from pathlib import Path
import json
import logging
from openai import OpenAI
from app.models import breed_classifier
from app.database import get_db
from ultralytics import YOLO
from app.models import dog_detection

chatgpt = OpenAI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

yolo = YOLO("yolo11n.pt")

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("landing.html")


@bp.get("/upload")
def upload_form():
    return render_template("upload-pet.html")


@bp.post("/new-pet")
def process_new_pet():
    try:
        upload_path = Path(current_app.config["UPLOAD_PATH"])

        image = request.files.get("pet-image")
        name = request.form.get("pet-name")
        age = request.form.get("pet-age")
        gender = request.form.get("pet-gender")

        image_id = store_image(image, upload_path)
        image_path = upload_path / f"{image_id}.{image.filename.split('.')[-1]}"

        detect_dog = dog_detection.detect_dog(yolo, image_path)
        dog_confidence = detect_dog["confidence"]
        if not detect_dog["detected"]:
            caption = f"Upon examination, we are only {dog_confidence:.2f}% certain that this is indeed a dog. But! "
        else:
            caption = f"We believe with {dog_confidence:.2f}% certainty that this is indeed a dog. "

        predicted_breed, confidence = get_custom_model_response(image_id)
        caption += f"Our breed classification model predicts that {name} is a {predicted_breed} with {confidence:.2f}% confidence"
        blurb = get_gpt_response(name, age, gender, predicted_breed)
        store_result(image_id, name, age, gender, predicted_breed, confidence)

        return render_template(
            "pet-result.html",
            id=image_id,
            caption=caption,
            blurb=blurb,
        )
    except Exception as e:
        logger.exception("problem with upload", e)
        return Response(
            json.dumps(
                {"status": "error", "message": "unable to process image upload"}
            ),
            status=500,
        )


@bp.get("/view-result")
def display_pet_result():
    return render_template("pet-result.html")


@bp.put("/feedback")
def accept_feedback():
    try:
        id = request.form.get("upload-id")
        is_correct = not request.form.get("is-wrong", False)
        actual_breed = request.form.get("actual-breed", "N/A")
        store_feedback(id, is_correct, actual_breed)
        return "Feedback accepted, thank you!"
    except Exception as e:
        logger.exception("Error saving feedback", e)
        return "Error accepting feedback!"


@bp.get("/breeds-list")
def get_breeds_selection():
    CLASS_NAME_JSON = current_app.config["MODEL_PATH"] / "class_names.json"
    with open(CLASS_NAME_JSON, "r") as f:
        breeds_obj = json.load(f)
        breeds_list = [v for k, v in breeds_obj.items()]
    return render_template("breed-select.html", breeds=breeds_list)


def store_image(image, upload_path):
    image_id = str(uuid4())
    extension = image.filename.split(".")[1]
    unique_filename = f"{image_id}.{extension}"
    logger.info("Saving file %s to %s", unique_filename, upload_path)
    image.save(upload_path / unique_filename)

    return image_id


def get_custom_model_response(image_id):
    response = breed_classifier.predict_breed(image_id)
    breed, confidence = response.get("breed", "???"), response.get("confidence", 0.00)

    return breed, confidence


def get_gpt_response(name, age, gender, breed):
    return "fake gpt"
    gpt_prompt = """
You will receive a JSON-formatted string with attributes of a dog. This dog is being listed for adoption by a shelter.
Write 5 sentences which reference the provided attributes, particularly the dog's name, age, gender, and breed.
The sentences should describe the dog and end by encouraging the reader to consider adopting them as a pet.

"""
    gpt_payload = json.dumps(
        {"name": name, "age": age, "gender": gender, "breed": breed}
    )

    response = chatgpt.responses.create(
        instructions=gpt_prompt, input=gpt_payload, model="gpt-4o-mini"
    )

    return response.output_text


def store_result(
    id, name, age, gender, predicted_breed, confidence, is_correct=3, actual_breed="N/A"
):
    insert_result = """
INSERT INTO Feedback (
    UploadID,
    Name,
    Age,
    Gender,
    PredictedBreed,
    Confidence,
    IsCorrect,
    ActualBreed)
VALUES (?, ?, ?, ?, ?, ?, ?, ?);
"""

    db = get_db()
    logger.info("Writing upload %s to Feedback table", id)
    db.execute(
        insert_result,
        (id, name, age, gender, predicted_breed, confidence, is_correct, actual_breed),
    )
    db.commit()


def store_feedback(id, is_correct, actual_breed):
    update_feedback = """
UPDATE Feedback
SET 
    IsCorrect = ?,
    ActualBreed = ?
WHERE UploadID = ?;
    """
    db = get_db()
    logger.info("Writing upload %s to Feedback table", id)
    db.execute(
        update_feedback,
        (is_correct, actual_breed, id),
    )
    db.commit()
