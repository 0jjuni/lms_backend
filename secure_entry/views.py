from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import User, Student, Professor
from .serializers import UserSerializer, StudentSerializer, ProfessorSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['enrollment_number'] = user.enrollment_number
        token['username'] = user.username
        if user.user_type == 'S':
            token['batch'] = user.student.batch.name
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def userDetail(request, enrollment_number):
    user = User.objects.filter(enrollment_number=enrollment_number).first()
    if user:
        if user.user_type == 'S':
            student = Student.objects.get(user=user)
            serializer = StudentSerializer(student)
        elif user.user_type == 'P':
            professor = Professor.objects.get(user=user)
            serializer = ProfessorSerializer(professor)
        else:
            return Response({'error': 'Invalid user type'}, status=400)
        return Response(serializer.data)
    return Response({'error': 'User not found'}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUserDetail(request):
    user = request.user
    if user.user_type == 'S':
        student = Student.objects.get(user=user)
        serializer = StudentSerializer(student)
    elif user.user_type == 'P':
        professor = Professor.objects.get(user=user)
        serializer = ProfessorSerializer(professor)
    else:
        return Response({'error': 'Invalid user type'}, status=400)
    return Response(serializer.data)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/secure_entry/token/',
        '/secure_entry/token/refresh/',
        'user/<str:enrollment_number>/',
        'user/me/'
        # '/secure_entry/change_password/'

    ]
    return Response(routes)