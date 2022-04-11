from flask import Blueprint, jsonify, request, render_template, Flask, request
from db import songs, populate
import json
import pickle
from views import categories
import os
from werkzeug.utils import secure_filename


rec_app = Blueprint('rec_app', __name__, template_folder='../static')

share_list = []

@rec_app.route('/playlist_gen')
def playlist_gen():
    return render_template('playlist_gen.html', categories=categories)


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

    return render_template(
        'playlist_ret.html', 
        playlist=playlist, 
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

UPLOAD_FOLDER = './save/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Parts of the following code was borrowed from the Flask documentation
# Allows user to import their song list
@app.route('/import', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        file = request.files['file']

        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            read = open("./save/" + filename, "r")
            v = read.read()
            j = json.loads(v)
            w = open("./save/" + filename, "w")
            w.write("")
            w.close()
            populate.populate_share(j)
            return v.encode()
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''