from pip import main
from reccomendation.algorithm import rec_algo

valid_features = ["genre_list", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"] #temporary

def res_get_playlist(in_dict: dict):
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
