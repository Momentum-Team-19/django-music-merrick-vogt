# accounts/views.py
from django.shortcuts import render, redirect
from .models import SpotifyUser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

def spotify_login(request):
    # Check if the user is already logged in
    if 'user_id' in request.session:
        return redirect('home')

    sp_oauth = SpotifyOAuth(
        client_id="3259917e1dfb4220abda16c477fc371a",
        client_secret="939c9bfd2d5c47c786af2456b1d6b536",
        redirect_uri="http://localhost:8000/accounts/spotify_login/",
        scope="user-library-read"
    )

    # Step 4: Check for the 'code' parameter in the URL query
    code = request.GET.get('code')

    if code:
        # Exchange 'code' for an access token
        token_info = sp_oauth.get_access_token(code=code)
    else:
        # Step 3: Check for a cached token or redirect to Spotify authorization page
        token_info = sp_oauth.get_cached_token()
        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            return redirect(auth_url)

    # Debugging token_info
    print(f"Token Info: {token_info}")

    # Your existing logic to log in the user using token_info
    token = token_info['access_token']
    sp = Spotify(auth=token)
    spotify_user = sp.current_user()

    user, created = SpotifyUser.objects.get_or_create(
        spotify_id=spotify_user['id'],
        defaults={'name': spotify_user['display_name']}
    )

    # You can set the user as a session variable to keep track of them
    request.session['user_id'] = user.id
    request.session['spotify_user_name'] = spotify_user['display_name'] 

    return redirect('playlists:home')  # Redirect to home view after Spotify login


