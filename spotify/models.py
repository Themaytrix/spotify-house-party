from django.db import models

# Create your models here.

class SpotifyToken(models.Model):
    # use session_id to identify user
    user = models.CharField(max_length=20,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)