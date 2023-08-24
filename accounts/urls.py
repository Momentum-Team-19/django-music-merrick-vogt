from django.urls import path
from . import views  # make sure to create views.py in your accounts app

urlpatterns = [
    # path('login/', views.spotify_login, name='login'),  # Custom login view
    path('spotify_login/', views.spotify_login, name='spotify_login')
    # path('logout/', views., name='logout'),  # Custom logout view
]