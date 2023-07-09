from django.urls import path
from .views import *


urlpatterns = [
    path('get-auth-url/', AuthUrl.as_view()),
    path('is-authenticated/', IsAunthenticated.as_view()),
    path('playing/',CurrentSong.as_view()),
    path('redirect/',SpotifyCallback.as_view()),
]
