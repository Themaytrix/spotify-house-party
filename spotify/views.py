from django.shortcuts import render,redirect
from .credentials import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request,post
from .util import *
from .serializers import SpotifySerializer,IsAuthenticatedSerializer
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
    def get(self,request,format=None):
        # get session_id from front end
        # use session_id to get the host
        endpoint = "player/currently-playing"
        
        pass