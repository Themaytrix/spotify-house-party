from rest_framework import serializers
from .models import Room,Listeners

class ListenersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listeners
        fields = ('active_room','listener')
        
class RoomSerializer(serializers.ModelSerializer):
    listeners = ListenersSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = ('id','name','host','votes_to_skip','created_at','id_session','listeners')


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name','votes_to_skip')
        

class JoinRoomSerializer(serializers.Serializer):
    id_session = serializers.CharField(max_length=50)
    id = serializers.IntegerField() 
    