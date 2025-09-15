import os
from dotenv import load_dotenv
from flask import Flask, request, redirect, session, render_template_string
import secrets
import urllib
import requests
import base64
import datetime

load_dotenv()  

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")
auth_url_base = os.getenv("AUTH_URL")
api_url_base = os.getenv("API_URL")
token_url = os.getenv("TOKEN_URL")
redirect_uri = os.getenv("REDIRECT_URI")


app = Flask(__name__)
app.secret_key = flask_secret_key  # for session management


@app.route('/')
def index():
    return "Welcome to the Spotify API Integration!"

@app.route('/login')
def request_authorization():
    """
    Request authorization from the user to access Spotify resources on the user's behalf. 
    To do this, send a GET request to the /authorize endpoint. 

    :return: 
      If success, user is redirected back to the redirect_uri (contains 2 params: code and state).
      If failure, the response string contains 2 params: error and state.
    """
    
    scope = 'user-library-read user-read-recently-played user-top-read playlist-read-private'
    state = secrets.token_urlsafe(16)

    params = {
      'client_id': client_id,
      'response_type': 'code',
      'redirect_uri': redirect_uri,
      'scope': scope,
      'state': state,
      'show_dialog': 'true'
    }

    # Build the authorization URL
    auth_url = f"{auth_url_base}?{urllib.parse.urlencode(params)}"

    print(f"Authorization URL: {auth_url}")


    return redirect(auth_url)


@app.route('/callback')
def callback():
  """
  Handle the callback from Spotify after user authorization.
  Exchange the authorization code for an access token by sending a POST request.

  :return:
    If success, returns 200 OK and token_info (contains access_token, token_type, expires_in, refresh_token, scope).
    If failure, returns error message.  
  """
  # if failure 
  if 'error' in request.args:
      error = request.args.get("error")
      return f"Error during authorization : {error}"
  
  # if success
  if 'code' in request.args:
    # print(f"Your authorization code is: {request.args.get('code')}")
    
    session['auth_code'] = request.args['code']
    return redirect('/auth_success')
 


@app.route('/auth_success')
def auth_success():
    auth_code = session.get('auth_code')

    session.pop("auth_code", None)


    return f"<h1>Authorization successful!</h1><p>Your code is: {auth_code}</p>"



@app.route('/refresh_token_form')
def refresh_token_form():
  """
  A form for the user to input the refresh token.
  """
  
  # simply send the form (containing token) to /resfresh_token/submit
  form_html = """
    <h2>Enter your refresh token</h2>
    <form action="/refresh_token/submit" method="post"> 
        <input type="text" name="input_refresh_token" placeholder="Enter the refresh token" required>
        <button type="submit">Submit</button>
    </form>
    """
  return render_template_string(form_html)

@app.route('/refresh_token/submit', methods=['POST'])
def refresh_token_submit():
    """
    Submit the form to refresh the access token.
    Send a POST request to the /api/token endpoint.
    """
    input_refresh_token = request.form.get("input_refresh_token")
    req_body = {
      "grant_type": "refresh_token",
      "refresh_token": input_refresh_token
    }

    # Encode client_id and client_secret in base64
    b64_auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {
      "Authorization": f"Basic {b64_auth}",
      "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(
      token_url,
      data = req_body,
      headers = headers
    )

    new_token_info = response.json()
    print("new token info:",new_token_info)

    return f"""<h1>Refresh successful!</h1>
            <p>Your new access token is: {new_token_info.get('access_token')}</p>
            <p>Your new refresh token is: {new_token_info.get('refresh_token')}</p>
            <p>Token expires at: {datetime.datetime.now() + datetime.timedelta(seconds=new_token_info.get('expires_in'))}</p>
           """



if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000, debug=True)