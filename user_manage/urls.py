from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('users/',RegisteredUserview.as_view(), name = 'users'),
    path('users/<int:pk>',RegisteredUserDetails.as_view(), name = 'Userdetail'),
    
    ]