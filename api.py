from typing import Dict
from pip import main


def res_get_playlist(in_dict: Dict):
    cleaned = {}
    for para in in_dict.keys():
        match para:
            case "genres":
                genres = []
                for g in in_dict["genres"]:
                    #Check if genre is listed by Spotify
                    #If so
                    cleaned["genres"].append(g)
                    #else signal to ser that the genre is invalid and continue without a genre
                if genres: cleaned["genres"] = genres
            case "acousticness": cleaned["acousticness"] = in_dict["acousticness"]
            case "danceability": cleaned["danceability"] = in_dict["danceability"]
            case "energy": cleaned["energy"] = in_dict["energy"]
            case "instrumentalness": cleaned["instrumentalness"] = in_dict["instrumentalness"]
            case "tempo": cleaned["tempo"] = in_dict["tempo"]
            case "valence": cleaned["valence"] = in_dict["valence"]
            case _:
                print("invalid item")
    return