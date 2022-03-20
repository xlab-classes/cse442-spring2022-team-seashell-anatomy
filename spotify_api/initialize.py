from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from credentials import client_id, secret_id

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, 
    client_secret=secret_id
)

search_data = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager
)
