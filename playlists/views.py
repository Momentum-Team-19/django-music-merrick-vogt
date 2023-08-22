from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import Playlist, Song  # Import your Playlist model if needed
from django.db import models

def home_view(request):
    return render(request, 'search/index.html')

# Define your Playlist model and playlist-related functions here
def get_playlist_by_id(playlist_id):
    # Implement logic to fetch playlist details from the database based on playlist_id
    # Return the playlist object
    return playlist_id

# Set up Spotify API client
client_credentials_manager = SpotifyClientCredentials(
    client_id='3259917e1dfb4220abda16c477fc371a',
    client_secret='939c9bfd2d5c47c786af2456b1d6b536'
)

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def search_results_view(request):
    print('Entered a search')
    query = request.GET.get('query')
    
    if query:
        # Search for tracks using Spotify API
        results = spotify.search(query, type='track', limit=10)
        tracks = results['tracks']['items']

        for track in tracks:
            print(f"Attempting to save track: {track['name']}")
            
            try:
                Song.objects.get_or_create(
                    title=track['name'],
                    album=track['album']['name'],
                    artist=track['artists'][0]['name'],  # Taking the first artist for simplicity
                    # spotify_id=track['id'],
                    # preview_url=track['preview_url']
                ) 
            except Exception as e:
                print(f"Error saving track {track['name']}: {e}")

    else:
        print("No query found")
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
