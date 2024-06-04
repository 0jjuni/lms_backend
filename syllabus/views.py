from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
# Create your views here.

#교수 권한
class IsProfessor(BasePermission):
    message = '과제등록은 교수님만 가능합니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'P'

class SyllabusCreateAPIView(generics.GenericAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerialziers
    permission_classes = [IsAuthenticated, IsProfessor]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
