from django.urls import path

from . import views

urlpatterns = [
    path('',views.RoomView.as_view()),
    path('create/',views.CreateRoom.as_view(), name='create'),
    path('<str:pk>/', views.JoinRoom.as_view(), name='room'),
    path('user-in-room/',views.UserInRoom.as_view(),name='user-in-room'),
]
