from flask import Flask, redirect, request, session
import requests

app = Flask(__name__)
app.secret_key = "random_secret_key"  # Needed for session

# Your Zenodo app credentials
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:5000/auth/callback"

# OAuth endpoints
AUTHORIZE_URL = "https://zenodo.org/oauth/authorize"
TOKEN_URL = "https://zenodo.org/oauth/token"

@app.route("/")
def index():
    # Redirect user to Zenodo authorization page
    auth_url = (
        f"{AUTHORIZE_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=deposit:write"
        f"&state=xyz123"
    )
    return redirect(auth_url)

@app.route("/auth/callback")
def callback():
    # Get the authorization code from Zenodo
    code = request.args.get("code")

    # Exchange code for access token
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, data=data)
    token_info = response.json()

    # Save token in session
    session["access_token"] = token_info["access_token"]

    return f"Access token: {token_info['access_token']}"

@app.route("/depositions")
def list_depositions():
    # Use the access token to call Zenodo API
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    r = requests.get("https://zenodo.org/api/deposit/depositions", headers=headers)
    return r.json()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
