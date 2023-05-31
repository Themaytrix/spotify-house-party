from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework import generics
from .models import Room
from .serializers import RoomSerializer,CreateRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Newuser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt
from houseparty import settings



# Create your views here.

class RoomView(APIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer 
    
    

class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer
    # authentication_classes = [JWTAuthentication]
    # 
    permission_classes = [IsAuthenticated]

    def post(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        serializer = CreateRoomSerializer(data=self.request.data)
        # user_id = self.request.session.get('user_id')
        # print(user_id)
        # try:
        #     host = Newuser.objects.get(id=user_id)
        # except Newuser.DoesNotExist:
        #     return Response({'Bad Request': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split('')[1]
        try:
            validated_token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = validated_token['user_id']
            host = Newuser.objects.get(id=user_id)
            
        except Newuser.DoesNotExist:
            return Response({'Bad Request': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

        
        if serializer.is_valid():
            
            id_session = self.request.session.session_key
            name = serializer.data.get('name')
            votes_to_skip = serializer.data.get('votes_to_skip')
            # check if user already hosting a room. we want to access it via existing session
            queryset = Room.objects.filter(id_session = id_session)
            if queryset.exists():
                room = queryset[0]
                room.name = name
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['name','votes_to_skip'])
                return Response(CreateRoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(name=name,host=host,id_session=id_session,votes_to_skip=votes_to_skip)
                room.save()
                return Response(CreateRoomSerializer(room).data,status=status.HTTP_200_OK)
                
        return Response({'Bad Request':'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user_id = request.user.id
        print(user_id)
            