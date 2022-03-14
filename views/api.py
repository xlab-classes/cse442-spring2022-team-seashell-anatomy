<<<<<<< HEAD
from pip import main
from reccomendation.algorithm import rec_algo

valid_features = set("genre_list", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature") #temporary

def res_get_playlist(in_dict):
    if not in_dict: return None
    cleaned = {}
    for feature in in_dict.keys():
        if feature in valid_features: 
            if feature == "genre_list": 
                cleaned_genres = in_dict[feature]
                if cleaned_genres is not list: return None
                cleaned[feature] = filter(res_filter_genres, cleaned_genres)
            else: cleaned[feature] = in_dict[feature]
    if not cleaned: return None
    #Get playlist with cleaned dictionary?
    playlist = rec_algo(in_dict)
    return playlist

def res_filter_genres(genre_string: str):
    if genre_string is "ska": return True
    else: return False

def res_add_rating(rating: int, description: str):
    #Enter rating into a database?
    return
=======
from typing import Dict


valid_features = ["acousticness", "danceability", "energy", "instrumentalness", "tempo", "valence"] #temporary

def res_get_playlist(in_dict: Dict):
    cleaned = {}
    for para in in_dict.keys():
        if para == "genres":
            genres = []
            for g in in_dict["genres"]:
                #Check if genre is listed by Spotify
                #If so
                cleaned["genres"].append(g)
                #else signal to ser that the genre is invalid and continue without a genre
            if genres: cleaned["genres"] = genres
        elif para in valid_features:
            cleaned[para] = in_dict[para]
        else:
            print("invalid entry: " + para)
    if not cleaned:
        return -1
    #Get playlist with cleaned dictionary?
    return 0
>>>>>>> 4b5683697ee854c8c7077a994d55d0dbd6b588b4
