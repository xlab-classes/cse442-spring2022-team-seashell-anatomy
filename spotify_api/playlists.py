from dotenv import load_dotenv
import json
import argparse
import os
import requests

load_dotenv(override=True)
sp = None

def get_token():
    return str(os.getenv("TOKEN"))

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
        "Authorization":"Bearer " + get_token()}
        )
    data = json.loads(response.text)
    return (data["external_urls"]["spotify"], data["id"])

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

