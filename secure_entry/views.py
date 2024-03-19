from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.response import Response
from .serializer import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse

# Create your views here.

def login(request) :
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(request, username=email, password=password)

        if user is None:
            print("회원이 아닙니다.")
            return redirect('/')
        else:
            auth.login(request, user)
            return redirect('/')

    return render(request, 'secure_entry/login.html')


def join(request) :
    print("join 실행!")
    if request.method == "POST" :
        print("여기는 포스트 요청")

        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(username=email, password=password)

        return redirect('/')

    print("join 마지막")
    return render(request, 'secure_entry/join.html')

def logout(request):

    auth.logout(request)

    return redirect('/')



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/secure_entry/token/',
        '/secure_entry/register/',
        '/secure_entry/token/refresh/'
    ]
    return Response(routes)