from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

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

# serves static files (we can have nginx do this in the future if we want)
@app.route('/static/<path>')
def render_static(path):
    with open(f'static/{path}') as file:
        return file
