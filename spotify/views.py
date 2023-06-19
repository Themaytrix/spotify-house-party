from django.shortcuts import render
from .credentials import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request,post
# Create your views here.

class AuthUrl(APIView):
    # get the url for authentication
    def get(self,requests,format=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-curently-playing'
        
        url = Request('GET','http://accounts.spotify.com/authorize',params={
            'scope':scopes,
            'response_type':'code',
            'redirect_uri':REDIRECT_URI,
            'client_id':CLIENT_ID,
        }).prepare().url
        
        return Response({'url':url}, status=status.HTTP_200_OK)
    
def spotify_callback(request,format=None):
    pass