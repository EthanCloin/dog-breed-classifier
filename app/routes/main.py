from flask import Blueprint, request, render_template, Response, current_app
from uuid import uuid4
from pathlib import Path
import json
import logging
from openai import OpenAI
from app.models import breed_classifier

chatgpt = OpenAI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("upload-pet.html")


@bp.post("/new-pet")
def process_new_pet():
    try:
        upload_path = Path(current_app.config["UPLOAD_PATH"])

        image = request.files.get("pet-image")
        name = request.form.get("pet-name")
        age = request.form.get("pet-age")
        gender = request.form.get("pet-gender")

        # return render_template("loading.html")

        image_id = store_image(image, upload_path)
        predicted_breed, confidence = get_custom_model_response(image_id)
        blurb = get_gpt_response(name, age, gender, predicted_breed)

        # TODO: tell the model to process the new image
        # TODO: return the updated webpage to await result.
        return render_template(
            "pet-result.html",
            id=image_id,
            caption=f"Our model predicts that {name} is a {predicted_breed} with {confidence:.2f}% confidence",
            blurb=blurb,
        )
        # return Response(
        #     json.dumps({"status": "success", "data": {"id": str(image_id)}}),
        #     status=202,
        #     content_type="application/json",
        # )
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


def store_image(image, upload_path):
    image_id = uuid4()
    extension = image.filename.split(".")[1]
    unique_filename = f"{image_id}.{extension}"
    logger.info("Saving file %s to %s", unique_filename, upload_path)
    image.save(upload_path / unique_filename)

    return str(image_id)


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


# def save_result(id, name, age, gender, predicted_breed, confidence, is_correct, actual_breed="N/A"):
#     result_file = current_app.config.get("RESULT_JSON")
#     with open(result_file, "r") as f:
#         json_results = json.load(f)
#         json_results[id] = {}
