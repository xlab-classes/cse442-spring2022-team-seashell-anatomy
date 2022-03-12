import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import credentials
import pickle

client_credentials_manager = SpotifyClientCredentials(client_id=credentials.client_id, client_secret=credentials.secret_id)
search_data = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# input the year and the desired number of songs from that year
def get_data(year, number_of_songs):
    track = search_data.search(q='year:'+str(year),type='track',limit=number_of_songs,market='us')
    full_list = []
    for k,i in enumerate(track['tracks']['items']):
        
        full_dictionary = {}
        
        #print statements for testing purposes
        #print("Image url: ", i['album']['images'][1]['url'])
        #print("Artist ID: ", i['album']['artists'][0]['id'])
        #print("Artist Name: ", i['artists'][0]['name'])
        #print("Song ID: ", i['id'])
        #print("Song Name: ", i['name'])
        #print(search_data.artist(i['album']['artists'][0]['id'])['genres'])
        
        # adding song name
        full_dictionary.update({"song_name":i['name']})

        #adding artist name
        full_dictionary.update({"artist_name":i['artists'][0]['name']})

        #adding spotify ID
        full_dictionary.update({"song_id":i['id']})

        #adding author's list of genres
        g_list = search_data.artist(i['album']['artists'][0]['id'])['genres']
        #Converts genre list to a pickle type.
        pickled = pickle.dumps(g_list)
        full_dictionary.update({"genre_list":pickled})

        #adding cover art url
        full_dictionary.update({"cover_url":i['album']['images'][1]['url']})

        #adding audio features
        features = search_data.audio_features(i['id'])
        
        #adding audio_attributes
        for k,v in features[0].items():
            full_dictionary.update({k:v})
        full_list.append(full_dictionary)
    return full_list
