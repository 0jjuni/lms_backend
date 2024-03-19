# 아래의 의미는 rest framework의 generics를 활용해,
# Mise테이블의 모든 데이터를 queryset을 통해 받아와
# 받아온 데이터의 모든 필드를(serializers.py에서 모든 필드를 설정했습니다.) MiseSerializer의 클래스를 사용하여
# json 데이터로 serialize한다는 의미입니다.

from django.shortcuts import render
#from .models import TotalLecture
# Create your views here.
from .models import TotalLecture
from .serializers import *
from rest_framework import generics


class TotalLectureListCreate(generics.ListCreateAPIView):
    queryset = TotalLecture.objects.all()
    serializer_class = TotalLectureSerializer


def home(request):
    lectures = TotalLecture.objects.all()

    return render(request,"sugang_register/home.html",{"lectures" : lectures})