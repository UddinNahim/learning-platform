import random
from django.shortcuts import render
from rest_framework import generics
from api import serializers as api_serializers
from rest_framework_simplejwt.views import TokenObtainPairView

from userauths.models import User, Profile
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializers.RegisterSeializer

def generate_random_otp(Length=7 ):
    otp = ''.join([str(random.randint(0,9)) for _ in range(Length)])
    return otp



class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user  = User.objects.get(email = email)

        if user:
            
            uuid64 = user.pk

            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f"http://localhost:5173/create-new-password/?otp{user.otp}&uuid64={uuid64}&=refresh_token{refresh_token}" 
            print("link ===",link)

        return user
    
    






