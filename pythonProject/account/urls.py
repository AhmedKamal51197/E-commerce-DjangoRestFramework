from django.urls import path
from .views import *



urlpatterns = [
    path('register/',register, name='register'),
    path('userinfo/',current_user,name='user_info'),
    path('userinfo/update/',updated_user,name="updated_user"),
    path('user/forgot-password/',forgot_password,name="forgot_password")
]
