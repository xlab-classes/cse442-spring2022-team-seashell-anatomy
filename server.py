from flask import Flask, request, render_template, session
from db import ENGINE, SONG_DATA, populate, songs
from views import static, rec, upvotes, auth
import random

import os, json
from flask import Flask, request
from werkzeug.utils import secure_filename
from db import populate

app = Flask(__name__)
app.secret_key = str(random.randint(0, 5))

# register views
app.register_blueprint(static.static_app)
app.register_blueprint(rec.rec_app)
app.register_blueprint(upvotes.upvotes_app)
app.register_blueprint(auth.auth_app)

UPLOAD_FOLDER = './save/'

# app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Parts of the following code was borrowed from the Flask documentation

@app.route('/import', methods=['GET', 'POST'])
def upload_file():
    print("enters here")
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
    return render_template("import.html")
