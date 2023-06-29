from django.urls import path
from .views import AuthUrl,IsAunthenticated


urlpatterns = [
    path('get-auth-url/', AuthUrl.as_view()),
    path('is-authenticated/', IsAunthenticated.as_view()),
    
]
