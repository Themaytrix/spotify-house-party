from django.shortcuts import render,redirect
from .credentials import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request,post
from .util import *
from .serializers import SpotifySerializer,IsAuthenticatedSerializer
from api.models import Room
# Create your views here.

class AuthUrl(APIView):
    # generating the url for the frontend to use for authentication
    def get(self,requests,format=None):
        scopes = 'user-read-playback-state user-modify-playback-state '
        
        url = Request('GET','https://accounts.spotify.com/authorize',params={
            'scope':scopes,
            'response_type':'code',
            'redirect_uri':REDIRECT_URI,
            'client_id':CLIENT_ID,
        }).prepare().url
        print(url)
        return Response({"url":url}, status=status.HTTP_200_OK)
    

    
class SpotifyCallback(APIView):
    def post(self,request,format=None):
        serializer = SpotifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data.get('code')
        print(code)
        id_session = serializer.validated_data.get('id_session')
        
        error = request.GET.get('error')
        # sending a post containing the code for the spotify token to the generated url
        response = post('https://accounts.spotify.com/api/token',data={
            'grant_type':'authorization_code',
            'code':code,
            'redirect_uri':REDIRECT_URI,
            'client_id':CLIENT_ID,
            'client_secret':CLIENT_SECRET,
            
        }).json()
        print(response)
        access_token = response.get('access_token')
        token_type = response.get('token_type')
        refresh_token = response.get('refresh_token')
        expires_in = response.get('expires_in')
        print(refresh_token)
        
    
        update_or_create_user_tokens(id_session,access_token,token_type,expires_in,refresh_token)
        
        return Response({"message":"User Authenticated by Spotify"})


class IsAunthenticated(APIView):
    def post(self,request,format=None):
        serializer = IsAuthenticatedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_session = serializer.validated_data.get('id_session')
        is_authenticated = is_spotify_authenticated(id_session)
        
        return Response({'status':is_authenticated}, status=status.HTTP_200_OK)
    
# music controller

class CurrentSong(APIView):
    def post(self,request,format=None):
        # get session_id from front end
        serializer = IsAuthenticatedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_session = serializer.validated_data.get('id_session')
        id_session = id_session[1:]
        room = Room.objects.filter(id_session=id_session)
        # if room.exists():
            
        #     room = room[0]
        # else:
        #     return Response({},status=status.HTTP_404_NOT_FOUND)

        # use session_id to get the host
        endpoint = "player/currently-playing/"
        response = spotify_api_calls(id_session,endpoint)
        
        if 'error' in response or not 'item' in response:
            return Response({},status=status.HTTP_204_NO_CONTENT)
        
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
            
        song = {
            'title': item.get('name'),
            'artist': artist_name_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'id': song_id
        }
                
        
        
        
        return Response(song,status=status.HTTP_200_OK)