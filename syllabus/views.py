from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from .serializers import SubjectSerializer
# Create your views here.

#교수 권한
class IsProfessor(BasePermission):
    message = '과제등록은 교수님만 가능합니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'P'

# 수강계획서 생성 (text만 채우기)
class SyllabusCreateAPIView(generics.GenericAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 수강계획서 보여주기
class TotalSyllabus(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        subject_code = request.query_params.get('subject_code')
        if not subject_code:
            return Response({"detail": "subject_code is required."}, status=status.HTTP_400_BAD_REQUEST)

        subject = get_object_or_404(Subject, subject_code=subject_code)
        syllabus = get_object_or_404(Syllabus, subject_code=subject)

        subject_serializer = SubjectSerializer(subject, context={'request': request})
        syllabus_serializer = SyllabusSerializer(syllabus, context={'request': request})

        data = {
            'subject': subject_serializer.data,
            'syllabus': syllabus_serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

#수강계획서 수정
class SyllabusUpdate(generics.UpdateAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_object(self):
        subject_code = self.kwargs.get('subject_code')
        return get_object_or_404(Syllabus, subject_code__subject_code=subject_code)


#수강계획서 삭제
class SyllabusDelete(generics.DestroyAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def get_object(self):
        subject_code = self.kwargs.get('subject_code')
        return get_object_or_404(Syllabus, subject_code__subject_code=subject_code)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "수강계획서가 성공적으로 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

