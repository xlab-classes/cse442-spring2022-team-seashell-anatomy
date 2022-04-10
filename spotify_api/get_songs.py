import requests
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv(), override=True)

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': os.environ.get('BEARER_TOKEN')
}


def parse_track(track):
    features_url = f'https://api.spotify.com/v1/audio-features/{track["id"]}'
    artists_url = track['artists'][0]['href']
    features = requests.get(features_url, headers=headers)
    artist = requests.get(artists_url, headers=headers)

    if features.status_code != 200 or artist.status_code != 200:
        raise ValueError

    print(f'GET {track["name"]}')

    return {
        'song_name': track['name'],
        'artist_names': track['artists'][0],
        'song_id': track['id'],
        'song_features': features.json(),
        'cover_art': track['album']['images'][0]['url'],
        'genres': artist.json()['genres']
    }


def get_songs_by_year(year, limit=None):
    url = f'https://api.spotify.com/v1/search?q=year%3D{year}&type=track'
    if limit:
        url += f'&limit={limit}'
    else:
        url += '&limit=100'

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError

    items = []
    while response.status_code == 200 and len(items) < limit:
        json_response = response.json()
        tracks = json_response['tracks']
        next = tracks['next']
        items += [parse_track(_) for _ in tracks['items']]
        response = requests.get(next, headers=headers)

    return items


def get_songs(n):
    yr = 2021
    retval = []
    
    while n > 0:
        songs = get_songs_by_year(yr, min(n, 100))
        retval += songs
        yr -= 1
        n -= len(songs)

    print(f'fetched {len(retval)} songs')
    return retval


if __name__ == '__main__':
    get_songs(10)
