from django.shortcuts import render,redirect
from .credentials import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request,post
from .util import update_or_create_user_tokens,is_spotify_authenticated
# Create your views here.

class AuthUrl(APIView):
    # generating the url for authentication
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
    code = request.GET.get('code')
    error = request.GET.get('error')
    # sending a post containing the code for the spotify token to the generated url
    response = post('http://accounts.spotify.com/api/token',data={
        'grant_type':'authorization_code',
        'code':code,
        'redirect_uri':REDIRECT_URI,
        'client_id':CLIENT_ID,
        'client_secret':CLIENT_SECRET,
        
    }).json()
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    eexpires_in = response.get('expires_in')
    
    if not request.session.exists(request.session.session_key):
        request.session.create()
    update_or_create_user_tokens(request.session.session_key,access_token,token_type,eexpires_in,refresh_token)
    
    return redirect({'frontend:'})


class IsAunthenticated(APIView):
    def get(self,requst,format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        
        return Response({'status':is_authenticated}, status=status.HTTP_200_OK)