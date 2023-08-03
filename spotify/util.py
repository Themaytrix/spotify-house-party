from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from requests import post, put, get
import json
import time
from .credentials import CLIENT_ID, CLIENT_SECRET
from django.core.serializers.json import DjangoJSONEncoder


BASE_URL = "https://api.spotify.com/v1/me/"


# get user tokens
def get_user_token(session_id):
    # check if there's a token for the user
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


# update or create user tokens
def update_or_create_user_tokens(
    session_id, access_token, token_type, expires_in, refresh_token
):
    tokens = get_user_token(session_id)
    # spotify token expires in 1hr(3600s) hence we create a time stamp to calculate duration
    print(expires_in)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.token_type = token_type
        tokens.expires_in = expires_in
        tokens.save(
            update_fields=["access_token", "refresh_token", "expires_in", "token_type"]
        )
    else:
        tokens = SpotifyToken(
            user=session_id,
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            token_type=token_type,
        )
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

    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).json

    access_token = response.get("access_token")
    token_type = response.get("token_type")
    expires_in = response.get("expires_in")
    refresh_token = response.get("refresh_token")

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token
    )


def spotify_api_calls(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_token(session_id)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + tokens.access_token,
    }

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    print(response.status_code)

    try:
        return response.json()
    except:
        return {"Error": "Issue with request"}


def playback_stream(id_session,endpoint):
    initial_data = ""
    
    while True:
        
        time.sleep(1)
        response = spotify_api_calls(session_id=id_session,endpoint=endpoint)
        
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
            
       
        data = json.dumps(response,cls=DjangoJSONEncoder)
        if not initial_data == data:
            yield "\ndata: " + "{}\n\n".format(data)
            initial_data = data
            
        