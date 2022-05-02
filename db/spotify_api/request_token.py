import requests
import os
from dotenv import load_dotenv, find_dotenv
import base64
import re


load_dotenv(find_dotenv(), override=True)


def regenerate_bearer_token():
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    token_url = 'https://accounts.spotify.com/api/token'

    credentials = f'{client_id}:{client_secret}'
    encoded_credentials = base64.b64encode(credentials.encode())

    token_data = {
        'grant_type': 'client_credentials'
    }
    token_headers = {
        'Authorization': f'Basic {encoded_credentials.decode()}'
    }

    response = requests.post(token_url, data=token_data, headers=token_headers)

    if response.status_code != 200:
        print(response.text)
        raise ValueError

    json = response.json()
    token_type, access_token = json['token_type'], json['access_token']

    bearer_token = f'{token_type} {access_token}'
    print(bearer_token)

if __name__ == '__main__':
    regenerate_bearer_token()

