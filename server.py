from flask import Flask, request, render_template, session
from db import ENGINE, SONG_DATA, populate, songs
from views import static, rec, upvotes, auth
import random

app = Flask(__name__)
app.secret_key = str(random.randint(0, 5))

# register views
app.register_blueprint(static.static_app)
app.register_blueprint(rec.rec_app)
app.register_blueprint(upvotes.upvotes_app)
app.register_blueprint(auth.auth_app)
