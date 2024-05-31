from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Subject
from .serializers import SubjectSerializer



# Create your views here.


class StudentEnrollmentList(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Enrollment.objects.filter(student__user=user)


class ProfessorSubjectList(generics.ListAPIView):
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Assuming Professor model has a OneToOne relation with User model or similar
        if hasattr(user, 'professor'):
            return Subject.objects.filter(professor__user=user)
        else:
            return Subject.objects.none()

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'enrollments/',
        'info/',
    ]
    return Response(routes)