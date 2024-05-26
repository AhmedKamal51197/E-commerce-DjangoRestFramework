from datetime import datetime, timedelta
from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.status import *
from .serializers import SignUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .models import Profile
# Create your views here.
@api_view(['POST'])
def register(req):
    data = req.data
    user = SignUpSerializer(data=data)
    if user.is_valid() :
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                username = data['email'],
                first_name= data['first_name'],
                last_name= data['last_name'],
                email = data['email'],
                password= make_password(data['password'])
            )
            return Response(status=HTTP_201_CREATED,data={'details' : 'register successfuly'})
        else :
            return Response(status=HTTP_400_BAD_REQUEST,data={'error':'this email already exists!'})
    else :
        return Response(user.errors)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(req):
    user = UserSerializer(req.user)
    print(user)
    return  Response({'userInfo':user.data}, status=HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updated_user(req):
    user = req.user
    data = req.data
    updatedUserSerializer= UserSerializer(user,data=data,partial=True)
    if updatedUserSerializer.is_valid():
        updatedUserSerializer.save()
        return Response({"msg":"Updated done"},status=HTTP_200_OK)
    else:
        return Response(updatedUserSerializer.errors,status=HTTP_400_BAD_REQUEST)



def get_current_host(req):
    protocol = req.is_secure() and 'https' or 'http'
    host = req.get_host()
    return  f"{protocol}://{host}"

@api_view(['POST'])
def forgot_password(req):
    data = req.data
    user = get_object_or_404(User,email=data['email'])

    token = get_random_string(40)
    expire_date = datetime.now()+timedelta(minutes=30)
    user.profile.rest_password_token = token
    user.profile.reset_password_expire =expire_date
    user.profile.save()
    host = get_current_host(req)
    link = f"{host}api/reset_password/{token}"
    body = f"Your password reset link is :{link}"
    send_mail(
        "password reset from eCommerce",
        body,
        "eCommerce@gmail.com",
        [data[" email"]]
    )
    #check evey time for "" or '' if ''
    return Response({'details' : f'password rset sent to {data["email"]}'})