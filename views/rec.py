from flask import Blueprint, jsonify, redirect, request, render_template, session, make_response
#from numpy import insert
from db import songs
from db import populate
import json
import pickle
from views import categories
from spotify_api import playlists
import random
import string
import json

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
    else:
        return render_template('request_song.html', error='This song is already in the database!')

    return redirect('/playlist_gen')

@rec_app.route('/generate')
def generate():
    share_list = []
    t = max(session.get('threshold', 0.8), 0.1)
    bias = max(min(session.get('bias', 0.0), 0.1), -0.1)
    print(t, bias)

    args = dict(request.args)

    name = args.pop('name')
    def gen_attrs():
        attrs = []
        for arg in args:
            attr_val = float(args[arg])  # specified attribute value
            lower = attr_val - t + bias  # lower threshold
            upper = attr_val + t + bias  # upper threshold
            attr_input = (arg, lower, upper)
            attrs.append(attr_input)
        return attrs

    attrs = gen_attrs()

    playlist = songs.get_songs_by_attrs(attrs)
    while len(playlist) < 10:
        t += 0.1
        attrs = gen_attrs()
        playlist = songs.get_songs_by_attrs(attrs)
        print(len(playlist))


    # print(playlist)

    cookie_song_list = []
    for e in playlist:
        json_format = {"id": e["id"], "song_name": e["song_name"], "song_id": e["song_id"]}
        cookie_song_list.append(e["id"])
        share_list.append(json_format)

    # handling cookies
    # adding cookies
    if request.cookies.get("old_songs"):
        new_list = json.loads(request.cookies.get("old_songs"))
        for i in new_list:
            cookie_song_list.append(i)
    
    # removing old playlists
    #for i in so
    #print("cookie id list", cookie_song_list)

    songlist = []
    for song in playlist:
        songlist.append(song["id"])
    letters = string.ascii_letters
    if not name:
        name = ''.join(random.choice(letters) for _ in range(10))
    link, pid = playlists.create_playlist(name, "Created with Seashell Resonance!")
    if link != None:
        playlists.add_songs_to_playlist(pid, songlist)
    else:
        link=''

    sharedata = {
        "playlist": share_list,
        "name": name
    }
    
    sharejson = json.dumps(sharedata)
    print(sharejson)
    response = make_response(render_template(
        'playlist_ret.html', 
        playlist=playlist,
        splink=link,
        name=name,
        share=sharejson,
        categories=[x['name'] for x in categories]
    ))

    response.set_cookie("old_songs", json.dumps(cookie_song_list))

    return response

def prev_songs():
    if request.cookies.get('old_songs'):
        return request.cookies.get('old_songs')
    else:
        return str([])
    

@rec_app.route('/artist', methods=['GET'])
def artist_songs():
    artist_name = request.args.get('a', type=str)
    song_list = songs.get_song_by_artist(artist_name)
    for song in song_list:
        song['genre_list'] = song['genre_list'] #Took out pickle.loads since the values in the database are lists (apparently).
    return jsonify(song_list), 200

@rec_app.route('/share', methods=['GET', 'POST'])
def share():
    
    playlists = songs.get_shared()
    if request.method == "GET":
        return render_template("share.html", title="Shared Playlists", songs=playlists)
    
    sharejson = request.form.get("sharedata")
    sharedata = json.loads(sharejson) 
    share_list = sharedata["playlist"]
    name = sharedata["name"]
    playlists = songs.get_shared()
    
    share_playlist = songs.get_playlist_with_id(share_list)
    print(share_playlist)
    #print(share_list)
    if songs.check_playlist(share_playlist) == -1:
        print("Playlist is a duplicate!")
    else:
        populate.populate_share(share_playlist, name)
        print("Populating...")
    
    share_list = []
    # playlists = songs.get_shared()
    # print(playlists)
            
    return render_template("share.html", title="Shared Playlists", songs=playlists)
