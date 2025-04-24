"""used to process the saved results from petfinder api"""

import csv
from pathlib import Path
import httpx
import json
from bs4 import BeautifulSoup
import os
import time


def main():
    json_files = [
        Path() / "data" / f for f in os.listdir(Path() / "data") if f.endswith(".json")
    ]
    output_file = Path() / "data" / "training" / "all_dog_data.csv"
    for file in json_files:
        start = time.time()
        parse_attributes_from_json(file, output_file)
        end = time.time()
        print(f"finished file {file.name} in {end - start:2f} seconds")


def save_image(download_url, save_path):
    if not download_url:
        return "NO URL PROVIDED"
    with httpx.stream("GET", download_url) as res:
        if not res.is_success:
            return "REQUEST FAILED"
        try:
            with open(save_path, "wb") as f:
                for chunk in res.iter_bytes():
                    f.write(chunk)
        except Exception:
            return "SAVE FAILED"
    return "SUCCESS"


def parse_attributes_from_json(input_path: Path, output_path: Path):
    """
    get images, descriptions (labels) and other attributes.
    """

    # input_path = Path() / "data" / str(input_filename + ".json")
    # output_path = Path() / "data" / str(output_filename + ".csv")
    # map attribute name to function which grabs data
    attributes = {
        "id": lambda x: x.get("id"),
        "breed": lambda x: x.get("breeds", {}).get("primary", None),
        "size": lambda x: x.get("size", None),
        "gender": lambda x: x.get("gender", None),
        "age": lambda x: x.get("age", None),
        "coat": lambda x: x.get("coat", None),
        # "status": lambda x: x.get("status", None),
        "name": lambda x: x.get("name", None),
        "good_w_children": lambda x: x.get("environment", {}).get("children", None),
        "good_w_dogs": lambda x: x.get("environment", {}).get("dogs", None),
        "good_w_cats": lambda x: x.get("environment", {}).get("cats", None),
        "house_trained": lambda x: x.get("attributes", {}).get("house_trained", None),
        "spayed_neutered": lambda x: x.get("attributes", {}).get(
            "spayed_neutered", None
        ),
        # description will require a webscraping
        "description": lambda x: parse_description_from_weblink(x.get("url")),
    }
    result_rows = []
    with open(input_path, "r") as f:
        result_batch = json.load(f)
        for animal in result_batch.get("animals", []):
            try:
                if animal is None:
                    continue

                row = {}
                for attr, getter in attributes.items():
                    row[attr] = getter(animal)

                image_prop = (
                    animal.get("primary_photo_cropped", {}) or {}
                )  # null value not caught by .get
                image_url = image_prop.get("small")

                image_path = (
                    Path() / "data" / "imgs" / str(str(row.get("id")) + ".jpeg")
                )
                row["image_status"] = save_image(image_url, image_path)

                result_rows.append(row)
            except Exception as e:
                print(e)

    columns = [k for k in attributes.keys()] + ["image_status"]
    if not output_path.exists():
        with open(output_path, "w") as o:
            writer = csv.DictWriter(o, fieldnames=columns, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerows(result_rows)
    else:
        with open(output_path, "a") as o:
            writer = csv.DictWriter(o, fieldnames=columns, quoting=csv.QUOTE_MINIMAL)
            writer.writerows(result_rows)


def parse_description_from_weblink(link):
    try:
        webpage = httpx.get(link)
        bs = BeautifulSoup(webpage.text, "html.parser")
        selected = bs.select("div.u-vr4x")
        description = selected[2].text

        return description
    except Exception as e:
        # print("scraping inconsistency {e}", e)
        return None


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Completed whole job in {end - start:.2f} seconds")
