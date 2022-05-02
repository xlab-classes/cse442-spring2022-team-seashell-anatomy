import os
import sys

import requests
from sqlalchemy import Float, PickleType, create_engine
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

DB_PATH = f'mysql+pymysql://{os.environ.get("USER")}:{os.environ.get("PASSWORD")}@{os.environ.get("SERVER")}'
META = MetaData()
ENGINE = create_engine(DB_PATH)
ENGINE.connect()

SONG_DATA = Table(
    'song_data', META, 
    Column('id_number', Integer, primary_key = True), 
    Column('song_name', String(255)), 
    Column('artist_name', String(255)),
    Column('artist_id', String(255)),
    Column('genre_list', PickleType),
    Column('cover_url', String(255)),
    Column('danceability', Float),
    Column('energy', Float),
    Column('key', Float),
    Column('loudness', Float),
    Column('mode', Float),
    Column('speechiness', Float),
    Column('acousticness', Float),
    Column('instrumentalness', Float),
    Column('liveness', Float),
    Column('valence', Float),
    Column('tempo', Float),
    Column('type', String(255)),
    Column('song_id', String(255)),
    Column('id', String(255)),
    Column('uri', String(255)),
    Column('track_href', String(255)),
    Column('analysis_url', String(255)),
    Column('duration_ms', Float),
    Column('time_signature', Integer),
    Column('rating', Float)
)

shared_playlists = Table(
    'shared_playlists', META, 
    Column('id_number', Integer, primary_key=True),
    Column('playlist_name', String(255)),
    Column('playlist', PickleType)
)

META.create_all(ENGINE)
SESSION = sessionmaker(bind=ENGINE)()


def parse_track(track):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': os.environ.get('BEARER_TOKEN')
    }
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
        'artist_id': track['artists'][0]['id'],
        'song_id': track['id'],
        'song_features': features.json(),
        'cover_url': track['album']['images'][1]['url'],
        'genre_list': artist.json()['genres']
    }


def get_songs_by_year(year, limit=None):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': os.environ.get('BEARER_TOKEN')
    }
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

def populate_database(num_songs):
    song_dict = get_songs(num_songs)  # Populates a list of dictionaries containing the song data.

    for f in song_dict:
        f.update(f['song_features'])
        f.pop('song_features')
        f['artist_name'] = ''.join(f['artist_name'])

    for i in range(num_songs):  # Populates the database with the number of songs
        ins = SONG_DATA.insert().values(**song_dict[i])
        conn = ENGINE.connect()
        conn.execute(ins)


def populate_share(share_list):
    ins = shared_playlists.insert().values(playlist=share_list)
    conn = ENGINE.connect()
    conn.execute(ins)


if __name__ == '__main__':
    # populate_database(100)
    pass
