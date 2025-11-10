from datetime import datetime
from flask import jsonify


def get_recently_played():
  if spotify_auth.access_token is None: # check if access_token is still valid
    return redirect('/login') # otherwise, re-login

  if datetime.now().timestamp() > spotify_auth.access_token_expiration_time: # the token is expired
    return redirect('/refresh_token') # redirect to refresh the token

  # get user's recently played tracks by including the following header
  headers = {
    "Authorization": f"Bearer {spotify_auth.access_token}"
  }

  response = requests.get(f"{api_url_base}/me/player/recently-played?limit=50", headers=headers) # current user's recently played tracks
  recently_played = response.json()

  return jsonify(recently_played)