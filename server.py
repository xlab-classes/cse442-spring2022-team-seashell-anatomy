from flask import Flask, request, render_template, session
from db import ENGINE, SONG_DATA, populate, songs
from views.api import res_get_playlist, res_add_rating

app = Flask(__name__)

categories = [
    {'name': 'acousticness', 'min': 0, 'max': 1, 'step': 0.01},
    {'name': 'danceability', 'min': 0, 'max': 1, 'step': 0.01},
    # {'name': 'duration_ms', 'min': 10, 'max': 1000000, 'step': 10},
    {'name': 'energy', 'min': 0, 'max': 1, 'step': 0.01},
    {'name': 'valence', 'min': 0, 'max': 1, 'step': 0.01}
]


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/static/<path>')
def render_static(path):
    with open(f'static/{path}') as file:
        return file


@app.route('/about')
def about():
    members = [
        {'name':'Emil Kovacev', 'major': 'Computer Science'},
        {'name': 'Kazi Shadman', 'major': 'Computer Science'},
        {'name': 'Steven Carter', 'major': 'Computer Science'},
        {'name': 'Jeffrey Naranjo', 'major': 'Computer Engineering'}, 
        {'name': 'Adam Russell', 'major': 'Computer Science'}
    ]
    return render_template('about.html', members=members)



@app.route('/playlist_gen')
def playlist_gen():
    data = request.json
    if data:
        song_list = data['songs']
        if 'songs_played' in session:
            previous_list = session.get('songs_played')
            for item in previous_list:
                song_list.append(item)
                
            session['songs_played'] = song_list
            
        else:
            session['songs_played'] = song_list
    return render_template('playlist_gen.html', categories=categories)



t = 0.3  # threshold

@app.route('/generate')
def generate():
    args = dict(request.args)
    attrs = [(x, float(args[x])-t, float(args[x])+t) for x in args]
    playlist = songs.get_songs_by_attrs(attrs)
    return render_template(
            'playlist_ret.html', playlist=playlist, 
            categories=[x['name'] for x in categories])


@app.route('/rating')
def rating():
    data = request.json
    song_id = data["song_id"]
    existing_rating = songs.get_song_by_id(song_id)["rating"]
    if existing_rating is None:
        ins = SONG_DATA.insert().values({"rating":1})
        conn = ENGINE.connect()
        conn.execute(ins)
    else:
        ins = SONG_DATA.insert().values({"rating":existing_rating + 1})
        conn = ENGINE.connect()
        conn.execute(ins)
    return render_template('rating.html')

