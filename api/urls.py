from django.urls import path

from . import views

urlpatterns = [
    path('',views.RoomView.as_view()),
    path('create/',views.CreateRoom.as_view(), name='create'),
    path('leave-room/',views.LeaveRoom.as_view()),
    path('delete-room/',views.EndRoom.as_view()),
    path('<str:pk>/', views.JoinRoom.as_view(), name='room'),

    
]
