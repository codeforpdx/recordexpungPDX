import io
import json
from google.protobuf.json_format import MessageToJson

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


class CharacterReader:
    @staticmethod
    def detect_document(path: str) -> str:
        """Detects document features in an image."""
        client = vision.ImageAnnotatorClient()

        with io.open(path, "rb") as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.document_text_detection(image=image)
        return json.loads(MessageToJson(response))["textAnnotations"][0]["description"].replace("\n", ",")
