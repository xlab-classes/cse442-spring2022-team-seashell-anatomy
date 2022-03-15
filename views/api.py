from pip import main
from reccomendation.algorithm import rec_algo

valid_features = ["genre_list", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"] #temporary

def res_get_playlist(in_dict: dict):
    if type(in_dict) is not dict: raise TypeError("Parameter entered is not a dictionary.")
    if not in_dict: raise ValueError("Dictionary entered is empty.")
    print("passed not in_dict")
    cleaned = {}
    for feature in in_dict.keys():
        if feature in valid_features: 
            if feature == "genre_list": 
                cleaned_genres = in_dict[feature]
                if type(cleaned_genres) is not list: raise TypeError('Value for "genre_list" is not a list')
                cleaned_genres = list(filter(res_filter_genres, cleaned_genres))
                if cleaned_genres: cleaned["genre_list"] = cleaned_genres
            else: cleaned[feature] = in_dict[feature]
    if not cleaned: raise ValueError("Input dictionary has no valid parameters")
    #Get playlist with cleaned dictionary?
    playlist = rec_algo(cleaned)
    print(cleaned)
    return playlist

def res_filter_genres(genre_string: str):
    if genre_string is "ska": return True
    else: return False

def res_add_rating(rating: int, description: str):
    #Enter rating into a database?
    return
