from rest_framework import serializers 
from .models import Newuser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newuser
        fields = ["username","email","password","is_active"]
        
        
        
class UserRegisterSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    
    class Meta:
        model = Newuser
        fields = ["username","password","email"]
    
