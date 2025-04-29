import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


class Config:
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    APP_BASE_PATH = Path() / "app"
    UPLOAD_PATH = APP_BASE_PATH / "static" / "uploads"
    MODEL_PATH = APP_BASE_PATH / "models" / "dog_breed_model"
    DATABASE_FILE = APP_BASE_PATH / "feedback.db"
    DETECTION_PATH = APP_BASE_PATH / "models" / "dog_detection"
