from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Student, Professor
from .serializers import UserSerializer, StudentSerializer, ProfessorSerializer
from .serializers import ChangePasswordSerializer, UserStudentSerializer, UserProfessorSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['enrollment_number'] = user.enrollment_number
        token['username'] = user.username
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['enrollment_number'] = self.user.enrollment_number
        data['username'] = self.user.username
        data['user_type'] = self.user.user_type
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([IsAdminUser])  # 이제 슈퍼유저만 접근 가능
def create_student(request):
    serializer = UserStudentSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_professor(request):
    serializer = UserProfessorSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'success': '비밀번호가 성공적으로 변경되었습니다..'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/secure_entry/token/',
        '/secure_entry/token/refresh/',
        '/secure_entry/create_student/',
        '/secure_entry/create_professor/',
        '/secure_entry/user/<str:enrollment_number>/',
        '/secure_entry/user/me/',
        '/secure_entry/change_password/',
    ]
    return Response(routes)
