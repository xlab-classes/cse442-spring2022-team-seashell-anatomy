from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/about')
def about():
    members = ['Emil Kovacev', 'Kazi Shadman', 'Steven Carter', 'Jeffrey Naranjo', 'Adam Russell']
    return render_template('about.html', members=members)

@app.route('/playlist_gen')
def playlist_gen():
    return render_template('playlist_gen.html')

# serves static files (we can have nginx do this in the future if we want)
@app.route('/static/<path>')
def render_static(path):
    with open(f'static/{path}') as file:
        return file
