from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

from .models import Announcement
from .serializers import announcementSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
class announcementCreateAPIView(generics.GenericAPIView):
    queryset = Announcement.objects.all()
    serializer_class = announcementSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class announcementUpdate(generics.UpdateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = announcementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

class annoucementDelete(generics.DestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = announcementSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        if obj.author != request.user:
            return Response({"권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/update/<int:pk>/',
        '/delete/<int:pk>/',

    ]
    return Response(routes)