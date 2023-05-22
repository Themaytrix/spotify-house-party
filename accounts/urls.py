from django.urls import path
from .views import UserList,MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', UserList.as_view()),
    path('api/token/', MyTokenObtainPairSerializer.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
