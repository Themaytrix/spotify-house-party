from django.db import models
import random
import string


# generate random code that is unique
def generate_unique_code():
    length = 6
    
    while True:
        # generate random code of length 6
        code = ''.join(random.choices(string.ascii_uppercase,k=length))
        # check if code is unique from  all other created rooms
        if Room.objects.filter(code = code).count() == 0:
            break
        
    return code
        



# Create your models here.
class Room(models.Model):
    code = models.CharField(max_length=8, default="", unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False,default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.host + "room"