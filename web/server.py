from flask import Flask, request, render_template, session
from db import ENGINE, SONG_DATA, populate, songs
from views import static, rec, upvotes

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

# register views
app.register_blueprint(static.static_app)
app.register_blueprint(rec.rec_app)
app.register_blueprint(upvotes.upvotes_app)
