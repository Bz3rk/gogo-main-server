from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from .serializers import DataSerializer, ClientRegistrationSerializer, DriverUpdateSerializer

from drf_spectacular.utils import extend_schema
from .models import CustomUser

# #import the custom user settings
# from django.conf import settings

# # #Assigning the custom user settings to a variable customuser
# CustomUser = settings.AUTH_USER_MODEL



# Create your views here.
@extend_schema(request = DataSerializer, responses = DataSerializer)
@api_view([ 'POST'])
def ClientLogin(request):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, email=request.data['email'])
        if not user.check_password(request.data['password']):
            return Response({"message": "Invalid credentials..."}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = DataSerializer(instance=user)
        return Response({'userData': serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
    return Response({})


@extend_schema(request = DataSerializer, responses = DataSerializer)
@api_view(['POST'])
def DriverLogin(request):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, email=request.data['email'])
        if not user.check_password(request.data['password']):
           return Response({"message": "Invalid credentials...."}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        serializer = DataSerializer(instance=user)
        return Response({'userData': serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
    return Response({})


@extend_schema(request = ClientRegistrationSerializer, responses = ClientRegistrationSerializer)
@api_view(['POST'])
def ClientRegister(request):
    if request.method == 'POST':
        serializer = ClientRegistrationSerializer(data = request.data, many=False)
        if serializer.is_valid():
            password = request.data['password']
            
            user = serializer.save( password=password)

            token = Token.objects.create(user=user)
            return Response({"userData": serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return Response({'Errors': serializer.errors})
    return Response({})


@extend_schema(request = DriverUpdateSerializer, responses = DriverUpdateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DriverRegister(request):
    if request.method == 'POST':
        user = request.user
        phone_no = request.data.get('phone_no')
        serializer = DriverUpdateSerializer(instance=user, data=request.data)
        serializer_user = DataSerializer(instance=user)

        if serializer.is_valid():
            serializer.save( phone_no=phone_no, is_driver=True)
            return Response({"userdata": serializer_user.data, "UpdateduserData": serializer.data}, status=status.HTTP_200_OK)
        return Response({'Errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({})


# @api_view(['POST'])
# def DriverRegister(request):
#     if request.method == 'POST':
#         serializer = DriverRegistrationSerializer(data = request.data, many=False)
#         if serializer.is_valid():            
#             password = request.data['password']
            
#             user = serializer.save( password=password)

#             token = Token.objects.create(user=user)
#             return Response({"userData": serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
#         return Response({'Errors': serializer.errors})
#     return Response({})

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response({"success":True})


