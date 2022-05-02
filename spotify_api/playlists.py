import base64
import json
import os
import time

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)
sp = None

state = os.getenv("state")
redirect_uri = os.getenv("redirect_uri")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def get_token():
    return os.environ.get("BEARER_TOKEN")

def update_token():
    url = "https://accounts.spotify.com/api/token"    
    param = {
        "grant_type": "refresh_token",
        "refresh_token": os.environ["refresh"]
    }
    auth = "Basic " + base64.b64encode((client_id + ":" + client_secret).encode("ascii")).decode("ascii")
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth
    }
    response = requests.post(url, data=param, headers=header)
    r = response.json()
    os.environ["access_token"] = r["access_token"]
    os.environ["refresh_time"] = str(time.time() + int(r["expires_in"]))

def create_playlist(name, desc):
    user_id = os.getenv("USERNAME")
    endpoint_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    request_body = json.dumps({
              "name": name,
              "description": desc,
              "public": True
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={
        "Content-Type":"application/json",
        "Authorization": get_token()}
    )
    data = json.loads(response.text)
    if data.get("external_urls"):
        return (data["external_urls"]["spotify"], data["id"])
    else:
        return (None, None)

def add_songs_to_playlist(pid, song_ids):
    endpoint_url = f"https://api.spotify.com/v1/playlists/{pid}/tracks"
    uris = []
    for song in song_ids:
        uris.append("spotify:track:" + song)
    request_body = json.dumps({
              "uris" : uris
            })
    response = requests.post(url = endpoint_url, data = request_body, headers={
        "Content-Type":"application/json",
        "Authorization":"Bearer " + get_token()}
        )

def create_playlist_from_songs():
    pass

if __name__ == "__main__":
    link, pid = create_playlist("test", "ing")
    add_songs_to_playlist(pid, ["4iV5W9uYEdYUVa79Axb7Rh", "1301WleyT98MSxVHPZCA6M"])

