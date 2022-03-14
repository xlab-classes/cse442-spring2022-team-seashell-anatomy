from flask import Flask, request, render_template
from db import populate, songs
from views.api import res_get_playlist, res_add_rating

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
        {'name': 'catA', 'min': 10, 'max': 12},
        {'name': 'catB', 'min': 10, 'max': 13}
    ]
    return render_template('playlist_gen.html', categories=categories)


@app.route('/generate')
def generate():
    playlist = res_get_playlist(request.args.to_dict(flat=False))
    return render_template('generate.html', playlist = playlist)

@app.route('/rating')
def rating():
    return render_template('rating.html')
