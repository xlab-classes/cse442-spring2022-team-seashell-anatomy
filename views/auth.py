from flask import Blueprint, jsonify, redirect, request, render_template, session
from urllib.parse import urlencode
import base64
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
auth_app = Blueprint('auth_app', __name__, template_folder='../static')

state = os.getenv("state")
redirect_uri = os.getenv("redirect_uri")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

@auth_app.route('/set_auth')
def set_auth():
    url = "https://accounts.spotify.com/authorize?"
    param = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": "playlist-modify-public playlist-modify-private"
    }
    red_url = url + urlencode(param)
    return redirect(red_url)

@auth_app.route('/get_code')
def get_code():
    url = "https://accounts.spotify.com/api/token"
    authcode = request.args.get("code")
    authstate = request.args.get("state")
    if authstate != state:
        return redirect('/')
    param = {
        "grant_type": "authorization_code",
        "code": authcode,
        "redirect_uri": redirect_uri
    }
    auth = "Basic " + base64.b64encode((client_id + ":" + client_secret).encode("ascii")).decode("ascii")
    header = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": auth
    }
    response = requests.post(url, data=param, headers=header)
    r = response.json()
    os.environ["refresh"] = r["refresh_token"]
    os.environ["access_token"] = r["access_token"]
    os.environ["refresh_time"] = str(time.time() + int(r["expires_in"]))
    return redirect('/')
