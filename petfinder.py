import httpx
from dotenv import load_dotenv
import os
import json
from pathlib import Path

ACCESS_TOKEN = "blank"
API_KEY = ""
SECRET = ""


def main():
    load_dotenv()
    global API_KEY, SECRET
    API_KEY = os.getenv("PETFINDER_API_KEY")
    SECRET = os.getenv("PETFINDER_SECRET")

    # get_petfinder_auth(API_KEY, SECRET)
    # get_dogs()
    for page in range(62, 101):
        get_dogs(page=page)


def get_petfinder_auth(api_key, secret):
    payload = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret,
    }
    url = "https://api.petfinder.com/v2/oauth2/token"

    response = httpx.post(url, data=payload)
    if response.is_success:
        with open("token.json", "w") as token_file:
            token: dict = response.json()
            print(type(token))
            json.dump(token, token_file)
            global ACCESS_TOKEN
            ACCESS_TOKEN = token.get("access_token", "")
    else:
        response.raise_for_status()


def get_dogs(is_retry=False, page=1):
    params = {
        "type": "Dog",
        "status": "adoptable,adopted,found",
        "location": "Jacksonville, FL",
        "distance": 500,
        "sort": "distance",
        "page": page,
        "limit": 100,
    }
    url = "https://api.petfinder.com/v2/animals"
    token_value = "Bearer " + ACCESS_TOKEN
    headers = {"Authorization": token_value}

    response = httpx.get(url, params=params, headers=headers)
    if response.is_success:
        content = response.json()
        animal_type = params.get("type")
        # city-state
        location = params.get("location", "").replace(", ", "-")
        # {page-num_animals_returned}
        page_and_count = (
            str(params.get("page", 1)) + "-" + str(len(content.get("animals", [])))
        )
        save_filename = f"{animal_type}_{location}_{page_and_count}.json"
        save_to_path = Path("data") / save_filename

        with open(save_to_path, "w") as f:
            json.dump(content, f)
    elif response.status_code == 401 and not is_retry:
        print("Auth Error! Refreshing token.")
        get_petfinder_auth(API_KEY, SECRET)
        get_dogs(is_retry=True)
    else:
        response.raise_for_status()


if __name__ == "__main__":
    main()
