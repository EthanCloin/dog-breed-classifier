import os
from pathlib import Path
import httpx
import json
from pprint import pprint
from bs4 import BeautifulSoup

img_dir = Path() / "data" / "imgs"

# res = httpx.get("https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/7970284/2/?bust=1291034096")
# with httpx.stream(
#     "GET", "https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/7970284/2/?bust=1291034096"
# ) as response:
#     with open(img_dir / "test.jpeg", "wb") as f:
#         for chunk in response.iter_bytes():
#             f.write(chunk)


def save_image(download_url, save_path):
    with httpx.stream("GET", download_url) as res:
        if not res.is_success:
            return "REQUEST FAILED"
        try:
            with open(save_path, "wb") as f:
                for chunk in res.iter_bytes():
                    f.write(chunk)
        except Exception:
            return "SAVE FAILED"
    return ""


def parse_attributes_from_json(filename=""):
    """get images, descriptions (labels) and other attributes"""

    filename = Path() / "data" / "Dog_Jacksonville-FL_1-100.json"
    # map attribute name to function which grabs data
    attributes = {
        "id": lambda x: x.get("id"),
        "breed": lambda x: x.get("breeds", {}).get("primary", None),
        "size": lambda x: x.get("size", None),
        "gender": lambda x: x.get("gender", None),
        "age": lambda x: x.get("age", None),
        "coat": lambda x: x.get("coat", None),
        "status": lambda x: x.get("status", None),
        "name": lambda x: x.get("name", None),
        # description will require a webscraping sheesh
        "description": lambda x: parse_description_from_weblink(x.get("url")),
    }
    result_rows = []
    with open(filename, "r") as f:
        result_batch = json.load(f)
        for animal in result_batch.get("animals", []):
            row = {}
            for attr, getter in attributes.items():
                row[attr] = getter(animal)
            result_rows.append(row)

    pprint(result_rows)


def parse_description_from_weblink(link):
    try:
        webpage = httpx.get(link)
        bs = BeautifulSoup(webpage.text, "html.parser")
        selected = bs.select("div.u-vr4x")

        # might need err handling here
        description: str = selected[2].text
        print("got desc of length " + str(len(description)))
        return description
    except Exception as e:
        print("scraping inconsistency {e}", e)
        return None


parse_attributes_from_json()
# parse_description_from_weblink(
#     "https://www.petfinder.com/dog/cammie-sc-20588208/fl/jacksonville/ratbone-rescues-southeast-region-fl138/?referrer_id=92d80cd8-084a-43cd-8f3d-ae87f8f918f1&utm_source=api&utm_medium=partnership&utm_content=92d80cd8-084a-43cd-8f3d-ae87f8f918f1"
# )
