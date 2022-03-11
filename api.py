from pip import main

valid_features = ["genre_list", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"] #temporary

def res_get_playlist(in_dict):
    cleaned = {}
    if in_dict: return []
    for feature in valid_features:
        if feature == "genre_list" and feature in in_dict: cleaned[feature] = in_dict[feature] #filter list
        elif feature in in_dict: cleaned[feature] = in_dict[feature]
    if not cleaned:
        return []
    #Get playlist with cleaned dictionary?
    return [{}]

def res_add_rating(rating: int, description: str):
    #Enter rating into a database?
    return