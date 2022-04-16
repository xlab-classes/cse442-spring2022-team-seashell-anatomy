from flask import Blueprint, jsonify, redirect, request, render_template
#from numpy import insert
from db import songs
from db import populate
import json
import pickle
from views import categories

share_list = []

rec_app = Blueprint('rec_app', __name__, template_folder='../static')


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

    if songs.get_song_by_uri(URI.decode('utf-8')) == -1:
        songs.insert_song(URI.decode('utf-8'))
    
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
        json_format = {"id": e["id"], "song_name": e["song_name"], "song_id": e["song_id"]}
        share_list.append(json_format)
    
    return render_template(
        'playlist_ret.html', 
        playlist=playlist, 
        categories=[x['name'] for x in categories]
    )

@rec_app.route('/artist', methods=['GET'])
def artist_songs():
    artist_name = request.args.get('a', type=str)
    song_list = songs.get_song_by_artist(artist_name)
    for song in song_list:
        song['genre_list'] = song['genre_list'] #Took out pickle.loads since the values in the database are lists (apparently).
    return jsonify(song_list), 200


@rec_app.route('/share')
def share():
    global share_list
    if len(share_list) != 0:
        share_playlist = songs.get_playlist_with_id(share_list)
        print(share_playlist)
        populate.populate_share(share_playlist)
        share_list = []
        playlists = songs.get_shared()
        print(playlists)
        display = ""
        for i,p in enumerate(playlists):
            song_names = []
            for song in p['playlist']:
                song_names.append(song['song_name'])

            display += ("<h1>" + "Playlist " + str(i) + "</h1>")
            display += '<br>'
            display += str(song_names)
            display += '<br>'
            display += '<br>'
            
        return str(display)
    else:
        return "No songs were shared yet".encode()
