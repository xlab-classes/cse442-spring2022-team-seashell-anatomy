from flask import Flask, request, render_template
from db import songs

app = Flask(__name__)


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
    categories = [
        {'name': 'energy', 'min': 0, 'max': 1, 'step': 0.01},
        {'name': 'danceability', 'min': 0, 'max': 1, 'step': 0.01}
    ]
    return render_template('playlist_gen.html', categories=categories)


@app.route('/generate')
def generate():
    args = dict(request.args)
    t = 0.1  # threshold
    attrs = [(x, float(args[x])-t, float(args[x])+t) for x in args]
    print(attrs)
    playlist = songs.get_songs_by_attrs(attrs)
    return render_template('playlist_ret.html', playlist=playlist)

