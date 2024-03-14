# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.settings import api_settings
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from user.serializers import CustomUserCreateSerializer, CustomUserLoginSerializer


def logout_view(request):
    logout(request)
    # Redirect to a login page, home page, or any other page
    return redirect('login_page')

def login_page(request):
    return redirect('login')

class UserCreateView(CreateAPIView):
    serializer_class = CustomUserCreateSerializer
    permission_classes = (AllowAny,)

class UserLoginView(GenericAPIView):
    serializer_class = CustomUserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.login(serializer)
        serialized_user_data = serializer.data
        serialized_user_data.update({
            'first_name': user.first_name,
            'last_name': user.last_name
        })
        headers = self.get_success_headers(serialized_user_data)
        return Response(serialized_user_data, status=status.HTTP_200_OK, headers=headers)

    def login(self, serializer):
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid Credentials')
        login(self.request, user)
        return user

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


