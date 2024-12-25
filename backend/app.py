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


@app.route('/login', methods=['GET'])
def login():
    """Initiate Spotify login process."""
    state = generate_random_state()
    scope = 'user-read-private user-read-email'

    auth_url = (
        'https://accounts.spotify.com/authorize?'
        f'client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}'
    )
    return jsonify({'url': auth_url})


@app.route('/callback', methods=['GET'])
def callback():
    """Handle Spotify callback with authorization code."""
    code = request.args.get('code')
    state = request.args.get('state')

    if not code:
        return jsonify({'error': 'Authorization code not received'}), 400

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return jsonify({'access_token': token_data['access_token']})
    else:
        return jsonify({'error': 'Failed to obtain token'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)


