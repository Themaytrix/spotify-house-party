from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer,CreateRoomSerializer
from rest_framework.views import APIView


# Create your views here.

class RoomView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 
    
    

class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer
    def post(self,request,format=None):
        pass