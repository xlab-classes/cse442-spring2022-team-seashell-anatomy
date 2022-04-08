from flask import Blueprint, render_template
from views import members


static_app = Blueprint('static_app', __name__, template_folder='../static')


@static_app.route("/")
def main():
    return render_template('index.html')


@static_app.route('/static/<path>')
def render_static(path):
    with open(f'static/{path}') as file:
        return file


@static_app.route('/about')
def about():
    return render_template('about.html', members=members)

