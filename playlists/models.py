from django.db import models
from accounts.models import SpotifyUser  # Import your custom User model

# Create your models here.

class Song(models.Model):
    spotify_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    # creator


    def __str__(self):
        return self.name
