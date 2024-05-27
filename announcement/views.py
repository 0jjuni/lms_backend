from django.shortcuts import render
from rest_framework import generics,status
from .models import Announcement
from .serializers import announcementSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# Create your views here.
class announcementCreateAPIView(generics.GenericAPIView):
    queryset = Announcement
    serializer_class = announcementSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class registerUpdate(generics.UpdateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = announcementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

