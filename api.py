from pip import main

valid_features = ["genre_list", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"] #temporary

def res_get_playlist(in_dict: dict) -> list:
    cleaned = {}
    for feature in valid_features:
        if feature == "genre_list" and in_dict[feature]: cleaned[feature] = in_dict[feature] #filter list
        elif in_dict[feature]: cleaned[feature] = in_dict[feature]
        else: print("Feature, " + feature + ", not found in input")
    if not cleaned:
        return []
    #Get playlist with cleaned dictionary?
    return [{"test": 42.0}]

def res_add_rating(rating: int, description: str):
    return