import requests
from dotenv import load_dotenv, find_dotenv
import os
import sys

from spotify_api.request_token import regenerate_bearer_token
from spotify_api.playlists import get_token

#regenerate_bearer_token()


#regenerate_bearer_token()
load_dotenv(find_dotenv(), override=True)

def getheaders():
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': "Bearer " + get_token()
    }
    return headers

def parse_track(track):
    headers = getheaders()
    features_url = f'https://api.spotify.com/v1/audio-features/{track["id"]}'
    artists_url = track['artists'][0]['href']
    features = requests.get(features_url, headers=headers)
    artist = requests.get(artists_url, headers=headers)

    if features.status_code != 200:
        print(features.text)
        raise ValueError

    if artist.status_code != 200:
        print(artist.text)
        raise ValueError


    print(f'GET {track["name"]}')

    return {
        'song_name': track['name'],
        'artist_name': track['artists'][0]['name'],
        'song_id': track['id'],
        'song_features': features.json(),
        'cover_url': track['album']['images'][1]['url'],
        'genre_list': artist.json()['genres']
    }


def get_one_song(id):
    headers = getheaders()
    track_url = f'https://api.spotify.com/v1/tracks/{id}'
    features_url = f'https://api.spotify.com/v1/audio-features/{id}'

    track_response = requests.get(track_url,headers=headers)
    json_response = track_response.json()
    track = json_response

    features = requests.get(features_url, headers=headers)
    artists_url = track['artists'][0]['href']
    artist = requests.get(artists_url, headers=headers)

    if features.status_code != 200:
        print(features.text)
        raise ValueError

    if artist.status_code != 200:
        print(artist.text)
        raise ValueError


    print(f'GET {track["name"]}')

    return {
        'song_name': track['name'],
        'artist_name': track['artists'][0]['name'],
        'song_id': track['id'],
        'song_features': features.json(),
        'cover_url': track['album']['images'][1]['url'],
        'genre_list': artist.json()['genres']
    }


def get_songs_by_year(year, limit=None):
    headers = getheaders()
    url = f'https://api.spotify.com/v1/search?q=year%3D{year}&type=track'
    url += '&limit=10'

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise ValueError

    items = []
    while response.status_code == 200:
        json_response = response.json()
        tracks = json_response['tracks']
        next = tracks['next']
        for track in tracks['items']:
            if len(items) >= limit:
                return items
            try:
                parsed = parse_track(track)
                items.append(parsed)
            except ValueError:
                print(f'ERROR {track["name"]}')
        response = requests.get(next, headers=headers)

    return items


def get_songs(n):
    yr = 2021
    retval = []
    
    while n > 0:
        print(yr)
        songs = get_songs_by_year(yr, n)
        retval += songs
        yr -= 1
        n -= len(songs)

    print(f'fetched {len(retval)} songs')
    return retval


if __name__ == '__main__':
    get_songs(int(sys.argv[1]))
