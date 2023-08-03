from django.urls import path,re_path

from .consumers import SpotifyConsumer

ws_urlpatterns =[
    path("spotify/<str:pk>/",SpotifyConsumer.as_asgi())
]