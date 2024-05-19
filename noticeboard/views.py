from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import NoticeBoardSerializer
from rest_framework import generics, status
from base.models import NoticeBoard


# Create your views here.

#NoticeBoard DB인스턴스 추가 ( 게시글 작성 )
class NoticeBoardCreateAPIView(generics.GenericAPIView):
    queryset = NoticeBoard.objects.all()
    serializer_class = NoticeBoardSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'noticeboard/create',

    ]
    return Response(routes)