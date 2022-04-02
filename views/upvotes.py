from flask import Blueprint, request, render_template
from db import ENGINE, SONG_DATA, songs


upvotes_app = Blueprint('upvotes_app', __name__, template_folder='../static')


@upvotes_app.route('/rating')
def rating():
    data = request.get_json()
    if not data or 'song_id' not in data:
        return ''

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


@upvotes_app.route('/toggle_upvote', methods=['POST'])
def toggle_upvote():
   json = request.get_json() 
   print(json)
   return '200'
