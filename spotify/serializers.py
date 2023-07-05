from rest_framework import serializers

class SpotifySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=250)
    id_session = serializers.CharField(max_length=50)
    
class IsAuthenticatedSerializer(serializers.Serializer):
    id_session = serializers.CharField(max_length=50)