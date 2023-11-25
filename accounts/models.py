from django.db import models

class SpotifyUser(models.Model):
    spotify_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    playlists = models.ManyToManyField('playlists.Playlist', related_name='users')


    def __str__(self):
        return self.name


