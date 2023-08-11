from channels.generic.websocket import  WebsocketConsumer
from asgiref.sync import async_to_sync,sync_to_async
from channels.exceptions import StopConsumer

from .util import spotify_api_calls
import json
import time


class SpotifyConsumer(WebsocketConsumer):
    
    
    
    def connect(self):
        
        id = self.scope['url_route']["kwargs"]['pk']
        self.room_group_name = id[1:]
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        # do something
        
        
        
    
    def receive(self, text_data=None):
        
        id_session = self.scope['url_route']['kwargs']['pk']
        id_session = id_session[1:]
        
        
        data = json.loads(text_data)
        _stream = data['message']
        message = {
            "id": id_session,
            "can_stream": _stream
        }    
        
        
        async_to_sync(self.channel_layer.group_send)(self.room_group_name,{"type": "send.stream","message": message})
            
            
            

        
    def send_stream(self,event):
        print(event)
        endpoint = "player/currently-playing/"
        data = event["message"]
        can_stream = data["can_stream"]
        id_session = data["id"]
        print(id_session)
        
        while can_stream:
            response = spotify_api_calls(session_id=id_session,endpoint=endpoint)
            
            if "error" in response or "item" not in response:
                return self.send(text_data=json.dumps({"message":{}}))
            
            if 'item' in response:
                item = response.get('item')
                duration = item.get('duration_ms')
                progress = response.get('progress_ms')
                album_cover = item.get('album').get('images')[0].get('url')
                is_playing = response.get('is_playing')
                song_id = item.get('id')
                artist_name_string = ""
            
            for i, artist in enumerate(item.get('artists')):
                if i > 0:
                    artist_name_string += ", "
                name = artist.get('name')
                artist_name_string += name
                
            response = {
                'title': item.get('name'),
                'artist': artist_name_string,
                'duration': duration,
                'time': progress,
                'image_url': album_cover,
                'is_playing': is_playing,
                'id': song_id
            }
            
            self.send(text_data=json.dumps({"message":response}))
            
            time.sleep(5)
        
        
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name,self.channel_name)
        
        raise StopConsumer()