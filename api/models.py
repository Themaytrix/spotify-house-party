from django.db import models

from users.models import Newuser

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=250, unique=True)
    host = models.ForeignKey(Newuser, on_delete=models.CASCADE, related_name="room")
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    id_session = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Listeners(models.Model):
    active_room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='listeners')
    listener = models.ForeignKey(Newuser, on_delete=models.CASCADE)
