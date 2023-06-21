from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import post
from .credentials import CLIENT_ID,CLIENT_SECRET


# get user tokens
def get_user_token(session_id):
    # check if there's a token for the user
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


# update or create user tokens
def update_or_create_user_tokens(session_id,access_token,token_type,expires_in,refresh_token):
    tokens = get_user_token(session_id)
    # spotify token expires in 1hr(3600s) hence we create a time stamp to calculate duration
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.token_type = token_type
        tokens.expires_in = expires_in
        tokens.save(update_fields=['access_token','refresh_token','expires_in','token_type'])
    else:
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            token_type=token_type)
        tokens.save()

# function to know if token has expired
def is_spotify_authenticated(session_id):
    tokens = get_user_token(session_id)
    if tokens:
        expiry = tokens.expires_in
        
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)  
        return True
    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_token(session_id).refresh_token
    
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type' : 'refresh_token',
        'refresh_token' : refresh_token,
        'client_id' : CLIENT_ID,
        'client_secret' : CLIENT_SECRET
    }).json
    
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')
    
    update_or_create_user_tokens(session_id,access_token,token_type,expires_in,refresh_token)