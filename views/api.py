from pip import main
from reccomendation.algorithm import rec_algo

valid_features = set("genre_list", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature") #temporary

def res_get_playlist(in_dict):
    if not in_dict: return None
    for feature in in_dict.keys():
        if feature not in valid_features: return None
    #Get playlist with cleaned dictionary?
    playlist = rec_algo(in_dict)
    return playlist

def res_add_rating(rating: int, description: str):
    #Enter rating into a database?
    return