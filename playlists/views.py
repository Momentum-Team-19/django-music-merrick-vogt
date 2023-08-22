from django.shortcuts import render, redirect
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import Playlist, Song  # Import your Playlist model if needed
from django.db import models
from django.http import HttpResponseBadRequest


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

# use query to search Spotify Api. 
    # danceability filter not implemented yet.
def search_results_view(request):
    print('Entered a search')
    query = request.GET.get('query')
    
    if query:
        # Search for tracks using Spotify API
        results = spotify.search(query, type='track', limit=10)
        tracks = results['tracks']['items']

    else:
        print("No query found")
        tracks = []

    return render(request, 'search/search_results.html', {'tracks': tracks})

# save tracks in local db
# store spotify_id as unique identifier
# function checks whether the song is already in database. 
def save_tracks_view(request):
    if request.method == "POST":
        # Extracting selected songs and the playlist name from the POST request
        selected_songs = request.POST.getlist('selected_songs')
        playlist_name = request.POST['playlist_name']

        # Create a new Playlist
        playlist = Playlist(name=playlist_name)
        playlist.save()

        # For each Spotify ID received
        for spotify_id in selected_songs:
            # Check if a Song with that Spotify ID already exists
            song, created = Song.objects.get_or_create(spotify_id=spotify_id)

            # If the song is newly created, fill in the details
            if created:
                 # Get the song details from the hidden input fields
                song.title = request.POST[f'track_{spotify_id}_name']
                song.album = request.POST[f'track_{spotify_id}_album']
                song.artist = request.POST[f'track_{spotify_id}_artist']
                song.save()

            # Associate the song with the new playlist
            playlist.songs.add(song)

        return redirect('playlists:playlist_detail', playlist_id=playlist.id)
    else:
        return HttpResponseBadRequest("Invalid request method")



# Define your playlist-related views here
def playlist_list_view(request):
    # Fetch a list of all playlists from the database
    playlists = Playlist.objects.all()
    return render(request, 'playlists/playlist_list.html', {'playlists': playlists})


def playlist_detail_view(request, playlist_id):
    playlist = Playlist.objects.get(pk=playlist_id)  # Fetch the specific playlist
    songs = playlist.songs.all()  # Fetch songs associated with the playlist

    context = {
        'playlist': playlist,
        'songs': songs,
    }
    
    return render(request, 'playlists/playlist_detail.html', context)

