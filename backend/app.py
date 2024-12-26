import os
import base64
import requests
from flask import Flask, request, redirect, jsonify, session
from flask_cors import CORS
from urllib.parse import urlencode
import random
import string
from dotenv import load_dotenv
app = Flask(__name__)
CORS(app)

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

REDIRECT_URI = os.getenv('REDIRECT_URI')

@app.route('/', methods=['GET'])
def check():
    return jsonify({"message": "Hello World!"})

def generate_random_state():
    """Generate a random string for Spotify state parameter."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


@app.route('/auth/spotify', methods=['GET'])
def spotify_auth():
    scope = 'user-read-private user-read-email'
    auth_url = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}'
    return jsonify({"auth_url": auth_url})


@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    code = data.get('code')
    redirect_uri = data.get('redirect_uri')

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)


