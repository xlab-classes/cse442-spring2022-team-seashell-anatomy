from flask import Blueprint, request, render_template
from db import ENGINE, SONG_DATA, songs


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

    elif song['content'] == 'downvote':
        new_rating = prev_rating - 1

    ins = SONG_DATA.insert().values({"rating": max(0, new_rating)})
    conn = ENGINE.connect()
    conn.execute(ins)

    print(f'{song} sent to db!')

    return '200'
