from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import TeamRecruitment
from .serializers import TeamRecruitmentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


class TeamRecruitmentCreateAPIView(generics.CreateAPIView):
    queryset = TeamRecruitment.objects.all()
    serializer_class = TeamRecruitmentSerializer

class TeamRecruitmentUpdateAPIView(generics.UpdateAPIView):
    queryset = TeamRecruitment.objects.all()
    serializer_class = TeamRecruitmentSerializer

class TeamRecruitmentViewSet(viewsets.ModelViewSet):
    queryset = TeamRecruitment.objects.all()
    serializer_class = TeamRecruitmentSerializer

    @action(detail=False, methods=['post'], url_path='search_by_title')
    def search_by_title(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

        team_recruitments = TeamRecruitment.objects.filter(title=title)
        if not team_recruitments:
            return Response({'error': 'No TeamRecruitment found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(team_recruitments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'team_connect/create/',
        'team_connect/update/<int:pk>/',
        'team_connect/',
        'team_connect/search-by-title/',
    ]
    return Response(routes)