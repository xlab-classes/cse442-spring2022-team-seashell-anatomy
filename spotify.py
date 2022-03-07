import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import credentials

client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id, client_secret=credentials.secret_id)
search_data = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_name = []
track_name = []
audio_features = []
track_id = []
for i in range(0,1):
    
    track = search_data.search(q='year:2020',type='track',limit=50,offset=i)
    for i, t in enumerate(track['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        audio_features.append(search_data.audio_features(t['id']))

#print(audio_features)