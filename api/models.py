from django.db import models

from users.models import Newuser
# import random
# import string


# generate random code that is unique
# def generate_unique_code():
#     length = 6
    
#     while True:
#         # generate random code of length 6
#         code = ''.join(random.choices(string.ascii_uppercase,k=length))
#         # check if code is unique from  all other created rooms
#         if Room.objects.filter(code = code).count() == 0:
#             break
        
#     return code
        



# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=250,unique=True)
    host = models.ForeignKey(Newuser,on_delete=models.CASCADE,related_name='room')
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    id_session = models.CharField(max_length=50, unique=True)
    
    def __str__(self) -> str:
        return self.name
    
class Listeners(models.Model):
    active_room = models.ForeignKey(Room,on_delete=models.CASCADE)
    listener = models.ForeignKey(Newuser,on_delete=models.CASCADE)
    