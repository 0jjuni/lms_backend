from django.shortcuts import render
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from rest_framework import generics, status, viewsets
from base.models import NoticeBoard


# Create your views here.

#NoticeBoard DB인스턴스 추가 ( 게시글 작성 )
class NoticeBoardCreateAPIView(generics.GenericAPIView):
    queryset = NoticeBoard.objects.all()
    serializer_class = NoticeBoardSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#게시판 정보 출력 view
class Noice_board_info(viewsets.ModelViewSet):
    #게시판에 대한 모든 정보 출력
    queryset = NoticeBoard.objects.all()
    serializer_class = NoticeBoardInfoSerializer

    # title을 이용한 게시글 찾기
    @action(detail=False, methods=['post'], url_path='search-by-title')
    def search_by_title(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'error': '제목을 작성하세요'}, status=status.HTTP_400_BAD_REQUEST)

        # title에 해당하는 모든 객체를 찾기
        NoticeBoard_instances = NoticeBoard.objects.filter(title=title)
        if not NoticeBoard_instances:
            return Response({'error': '게시글을 찾지 못했습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 찾은 인스턴스 직렬화
        serializer = self.get_serializer(NoticeBoard_instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#게시판 업데이트
class NoticeBoardUpdateAPIView(generics.UpdateAPIView):
    queryset = NoticeBoard.objects.all()
    serializer_class = NoticeBoardSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        serializer = self.get_serializer(obj, data=request.data, partial=False)  # Update the entire instance
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 게시판 삭제 view
class NoticeBoardDestroyAPIView(generics.DestroyAPIView):
    queryset = NoticeBoard.objects.all()
    serializer_class = NoticeBoardSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create',
        '/update/<int:pk>/',
        '/destroy/<int:pk>/',
        '/info',
        '/info/noticeboard/',
        '/info/noticeboard/search-by-title',
    ]
    return Response(routes)

