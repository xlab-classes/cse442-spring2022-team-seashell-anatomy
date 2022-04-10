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
    url = f'https://api.spotify.com/v1/audio-features/{track["id"]}'
    print(f'GET {url}')
    features = requests.get(url, headers=headers)
    if features.status_code != 200:
        print(features.text)
        raise ValueError

    return {
        'song_name': track['name'],
        'artist_names': [x['name'] for x in track['artists']],
        'song_id': track['id'],
        'song_features': features.json()
    }


def get_songs_by_year(year, limit=None):
    url = f'https://api.spotify.com/v1/search?q=year%3D{year}&type=track'
    if limit:
        url += f'&limit={limit}'

    print(f'GET {url}')
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError

    items = []
    while response.status_code == 200 and len(items) < limit:
        json_response = response.json()
        tracks = json_response['tracks']
        next = tracks['next']
        items += [parse_track(_) for _ in tracks['items']]
        print(f'GET {next}')
        response = requests.get(next, headers=headers)

    return items


def get_songs(n):
    yr = 2021
    retval = []
    
    while n > 0:
        songs = get_songs_by_year(yr, min(n, 10))
        retval += songs
        yr -= 1
        n -= len(songs)

    print(f'fetched {len(retval)} songs')
    return retval


if __name__ == '__main__':
    get_songs(10000)
