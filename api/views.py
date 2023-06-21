from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics
from .models import Room,Listeners
from .serializers import RoomSerializer, CreateRoomSerializer, JoinRoomSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.models import Newuser
from django.http import JsonResponse

# Create your views here.


class RoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        rooms =Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = CreateRoomSerializer(data=request.data)

        host = Newuser.objects.get(id=self.request.user.id)

        if serializer.is_valid():
            id_session = self.request.session.session_key
            name = serializer.data.get("name")
            votes_to_skip = serializer.data.get("votes_to_skip")
            # check if user already hosting a room. we want to access it via existing session
            queryset = Room.objects.filter(id_session=id_session)
            if queryset.exists():
                room = queryset[0]
                room.name = name
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["name", "votes_to_skip"])
                self.request.session['room_key'] = room.id_session
                return Response(
                    CreateRoomSerializer(room).data, status=status.HTTP_200_OK
                )
            else:
                room = Room(
                    name=name,
                    host=host,
                    id_session=id_session,
                    votes_to_skip=votes_to_skip,
                )
                room.save()
                self.request.session['room_key'] = room.id_session
                return Response(
                    CreateRoomSerializer(room).data, status=status.HTTP_200_OK
                )

        return Response(
            {"Bad Request": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
        )


class JoinRoom(APIView):
    def post(self, request, pk,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = JoinRoomSerializer(data=request.data)
        

        serializer.is_valid(raise_exception=True)
        id_session = serializer.validated_data.get("id_session")


        try:
            room = Room.objects.get(id_session=id_session)
            
            listener = Newuser.objects.get(id=self.request.user.id)
            queryset = room.listeners.filter(listener=self.request.user.id)
            print(queryset)
            
            # check if the room exists
            # get the listeneres of a room
            # if it exists we want to access the listeners in the room
            # if a listener is new we write to the db
            
            
            # print(len(queryset))
            # if len(queryset) == 0:
            #     active_listener = Listeners(
            #         active_room=room,
            #         listener=listener
            #     )
            #     active_listener.save()
            self.request.session['room_key'] = id_session
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
        except Room.DoesNotExist():
            return Response({"Room does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
    def get(self,request,pk,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create() 
        pk = pk[1:]
        active_room = Room.objects.get(id=pk)
        serializer = RoomSerializer(active_room,many=False)   
        
        return Response(serializer.data)
    
class UserInRoom(APIView):
    def get(self,request,format=None):
        # check to see if room_key exists in user's session
        data = {
            'room_key' : self.request.session.get('room_key')
        }
        
        return JsonResponse(data,status=status.HTTP_200_OK)
            



