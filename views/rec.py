from flask import Blueprint, request, render_template
from db import songs
from views import categories


rec_app = Blueprint('rec_app', __name__, template_folder='../static')


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
    print(playlist)
    return render_template(
        'playlist_ret.html', 
        playlist=playlist, 
        categories=[x['name'] for x in categories]
    )

