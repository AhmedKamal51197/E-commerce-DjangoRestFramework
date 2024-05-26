from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.status import *
from .serializers import SignUpSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated
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
    return  Response({'userInfo':user.data}, status=HTTP_200_OK)
