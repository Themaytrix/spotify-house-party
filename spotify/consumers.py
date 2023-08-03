from channels.generic.websocket import AsyncWebsocketConsumer
from .util import spotify_api_calls


class SpotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.accept()
        print('connected')