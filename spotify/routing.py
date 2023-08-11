from django.urls import path,re_path

from .consumers import SpotifyConsumer

ws_urlpatterns =[
    path("ws/spotify/<str:pk>/",SpotifyConsumer.as_asgi())
]