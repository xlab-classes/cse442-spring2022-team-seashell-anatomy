from flask import Blueprint, jsonify, redirect, request, render_template
from db import songs
import json
import pickle
from views import categories
from spotify_api import playlists
import random
import string
rec_app = Blueprint('rec_app', __name__, template_folder='../static')

share_list = []

@rec_app.route('/playlist_gen')
def playlist_gen():
    return render_template('playlist_gen.html', categories=categories)

@rec_app.route('/requestform')
def request_form():
    return render_template('request_song.html', error='')

@rec_app.route('/request')
def request_song():
    URL = request.query_string
    URLsplit = URL.split(b'%2F') #split by '/'
    if not len(URLsplit) >= 3 or not URLsplit[2] == b"open.spotify.com":
        return render_template('request_song.html', error='INVALID URL: Not from Spotify')
    if not len(URLsplit) >= 4 or not URLsplit[3] == b'track':
        return render_template('request_song.html', error='INVALID URL: URL not from a track')
    URI = URLsplit[-1].split(b'%3F')[0] #split by '?'
    if not URI or not len(URI) == 22:
        return render_template('request_song.html', error='INVALID URL: Invalid track ID')
    return redirect('/playlist_gen')


# attribute: a parameter for the spotify API
#   ex: dancability
#
#
# threshold (t): bounds for the parameter to be searched
# ex: 
#   if:
#       danceability = 0.5
#       threshold = 0.1
#       
#   then:
#       search for danceability in the range 0.4 < danceability < 0.6

@rec_app.route('/generate')
def generate():
    t = 0.3  # argument threshold

    args = dict(request.args)
    attrs = []
    for arg in args:
        attr_val = float(args[arg])  # specified attribute value
        lower = attr_val - t  # lower threshold
        upper = attr_val + t  # upper threshold
        attr_input = (arg, lower, upper)
        attrs.append(attr_input)

    playlist = songs.get_songs_by_attrs(attrs)

    for e in playlist:
        json_format = {"id_number": e["id_number"], "song_name": e["song_name"], "song_id":e["song_id"]}
        share_list.append(json_format)

    songlist = []
    for song in playlist:
        songlist.append(song["id"])
    letters = string.ascii_letters
    name = ''.join(random.choice(letters) for i in range(10))
    link, pid = playlists.create_playlist(name, name)
    print(link)
    playlists.add_songs_to_playlist(pid, songlist)

    return render_template(
        'playlist_ret.html', 
        playlist=playlist,
        splink=link,
        categories=[x['name'] for x in categories]
    )



@rec_app.route('/share')
def share():
    if len(share_list) != 0:
        return str(share_list)
    else:
        return "No songs were shared yet".encode()

@rec_app.route('/artist', methods=['GET'])
def artist_songs():
    artist_name = request.args.get('a', type=str)
    song_list = songs.get_song_by_artist(artist_name)
    for song in song_list:
        song['genre_list'] = pickle.loads(song['genre_list'])
    return jsonify(song_list), 200


