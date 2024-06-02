from django.shortcuts import render
from rest_framework.decorators import api_view

from .serializers import *
from .models import lecture
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from django.http import FileResponse
# Create your views here.

# 교수님 권한 검사
class IsProfessor(BasePermission):
    message = '강의자료 작성은 교수님만 가능합니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'P'
# 강의자료 생성
class lectureCreateAPIView(generics.GenericAPIView):
    queryset = lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 강의자료 Read
class LectureInfo(generics.ListAPIView):
    queryset = lecture.objects.all()
    serializer_class = LectureInfo
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = lecture.objects.all()
        author = self.request.query_params.get('author')
        title = self.request.query_params.get('title')
        subject_code = self.request.query_params.get('subject_code')

        if author:
            queryset = queryset.filter(author__username__icontains=author)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if subject_code:
            queryset = queryset.filter(subject_code=subject_code)

        return queryset

# 강의자료 update
class LectureUpdate(generics.UpdateAPIView):
    queryset = lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        result = self.queryset.filter(author=self.request.user)
        if not result.exists():
            raise serializers.ValidationError("작성자가 작성한 게시글이 없습니다")
        return result

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# 강의자료 delete
class LectureDelete(generics.DestroyAPIView):
    queryset = lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        if obj.author != request.user:
            return Response({"권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        obj.delete()  # 객체를 삭제합니다.
        return Response({"detail": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

class LectureFileDownloadAPIView(generics.GenericAPIView):
    queryset = lecture.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        register_instance = self.get_object()
        file_handle = register_instance.upload.path
        response = FileResponse(open(file_handle, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{register_instance.upload.name}"'
        return response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/read/',
        '/download/<int:pk>/'
        '/update/<int:pk>/',
        '/delete/<int:pk>/',

    ]
    return Response(routes)