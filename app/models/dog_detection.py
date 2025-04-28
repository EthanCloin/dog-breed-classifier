import logging

logger = logging.getLogger(__name__)


def detect_dog(yolo, image):
    try:
        results = yolo(image)
        confidence = 0.0

        for result in results:
            for box in result.boxes:
                if box.cls == 0:
                    confidence = max(confidence, float(box.conf))

        return {
            "detected": confidence > 0.5,
            "confidence": confidence,
        }

    except Exception as e:
        logger.exception("Error during dog detection", exc_info=e)
        return {
            "detected": False,
            "confidence": 0.0,
        }
