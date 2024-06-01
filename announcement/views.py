from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from .models import Announcement
from .serializers import AnnouncementSerializer, AnnouncementInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers
# Create your views here.

#공지사항 등록
class AnnouncementCreateAPIView(generics.GenericAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#공지사항 Read기능
class AnnouncementInfo(generics.ListAPIView):
    serializer_class = AnnouncementInfo
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Announcement.objects.all()
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

# 공지사항 수정
class AnnouncementUpdate(generics.UpdateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        result = self.queryset.filter(author=self.request.user)
        if not result.exists():
            raise serializers.ValidationError("작성자가 작성한 게시글이 없습니다")
        return result


# 공지사항 삭제
class AnnoucementDelete(generics.DestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        if obj.author != request.user:
            return Response({"권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        obj.delete()  # 객체를 삭제합니다.
        return Response({"detail": "삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/read/',
        '/update/<int:pk>/',
        '/delete/<int:pk>/',

    ]
    return Response(routes)