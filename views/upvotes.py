from flask import Blueprint, request
from db import ENGINE, SONG_DATA, songs
from flask import session

from . import categories


upvotes_app = Blueprint('upvotes_app', __name__, template_folder='../static')

# {'song_id': '5E8remXZPiYuvZEzavW4lT', 'content': 'upvote'}
@upvotes_app.route('/toggle_upvote', methods=['POST'])
def toggle_upvote():
    song = request.get_json()
    
    if not song:
        return ''

    song_id = song['song_id']
    prev_rating = songs.get_song_by_id(song_id)['rating']
    if prev_rating is None:
        prev_rating = 0

    if song['content'] == 'upvote':
        new_rating = prev_rating + 1
        threshold = session.get('threshold', 0.8) - 0.01
        session['threshold'] = threshold
        db_song = songs.get_song_by_id(song_id)
        bias = sum([db_song[cat['name']] - threshold for cat in categories]) * 0.1
        
        print(bias, threshold)


        session['bias'] = min(max(session.get('bias', 0.0) + bias, 0.3), -0.3)
    elif song['content'] == 'downvote':
        new_rating = prev_rating - 1
    else:
        new_rating = 0

    ins = SONG_DATA.insert().values({"rating": max(0, new_rating)})
    conn = ENGINE.connect()
    conn.execute(ins)

    print(f'{song} sent to db!')

    return '200'
