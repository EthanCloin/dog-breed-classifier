import httpx
from dotenv import load_dotenv
import os
import json


def main():
    load_dotenv()
    API_KEY = os.getenv("PETFINDER_API_KEY")
    SECRET = os.getenv("PETFINDER_SECRET")

    get_petfinder_auth(API_KEY, SECRET)


def get_petfinder_auth(api_key, secret):
    """
    curl -d "grant_type=client_credentials&client_id={CLIENT-ID}&client_secret={CLIENT-SECRET}" https://api.petfinder.com/v2/oauth2/token
    """
    payload = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret,
    }
    url = "https://api.petfinder.com/v2/oauth2/token"

    response = httpx.post(url, data=payload)
    if response.is_success:
        with open("token.json", "w") as token_file:
            json.dump(response.json(), token_file)


if __name__ == "__main__":
    main()
