from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.


class StudentEnrollmentList(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Enrollment.objects.filter(student__user=user)




@api_view(['GET'])
def getRoutes(request):
    routes = [
        'enrollments/',
    ]
    return Response(routes)