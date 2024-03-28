from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.response import Response
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializer import ChangePasswordSerializer
# Create your views here.


def logout(request):

    auth.logout(request)

    return redirect('/')



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

# class ChangePasswordView(generics.UpdateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = ChangePasswordSerializer
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)
#
#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.validated_data.get('old_password')):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # Set new password
#             self.object.set_password(serializer.validated_data.get('new_password'))
#             self.object.save()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer




@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/secure_entry/token/',
        '/secure_entry/register/',
        '/secure_entry/token/refresh/',
        '/secure_entry/change_password/'
    ]
    return Response(routes)