from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

from dotenv import load_dotenv
import os
load_dotenv(override=True)

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, 
    client_secret=client_secret
)

search_data = spotipy.Spotify(client_credentials_manager=client_credentials_manager)