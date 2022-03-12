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
