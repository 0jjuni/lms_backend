

# Create your views here.
from .models import TotalLecture
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response



class TotalLectureListCreate(generics.ListCreateAPIView):
    queryset = TotalLecture.objects.all()
    serializer_class = TotalLectureSerializer



@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/sugang_register/lecture_info/'
    ]
    return Response(routes)