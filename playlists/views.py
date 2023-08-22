from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import Playlist  # Import your Playlist model if needed

def home_view(request):
    return render(request, 'search/index.html')

# Define your Playlist model and playlist-related functions here
def get_playlist_by_id(playlist_id):
    # Implement logic to fetch playlist details from the database based on playlist_id
    # Return the playlist object
    return playlist_id

# Set up Spotify API client
client_credentials_manager = SpotifyClientCredentials(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET'
)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_results_view(request):
    query = request.GET.get('query')
    
    if query:
        # Search for tracks using Spotify API
        results = spotify.search(query, type='track', limit=10)
        tracks = results['tracks']['items']
    else:
        tracks = []

    return render(request, 'search/search_results.html', {'tracks': tracks})

# Define your playlist-related views here
def playlist_list_view(request):
    # Fetch a list of all playlists from the database
    playlists = Playlist.objects.all()
    return render(request, 'playlists/playlist_list.html', {'playlists': playlists})

def playlist_detail_view(request, playlist_id):
    # Fetch details of a specific playlist from the database using get_playlist_by_id
    playlist = get_playlist_by_id(playlist_id)
    return render(request, 'playlists/playlist_detail.html', {'playlist': playlist})
