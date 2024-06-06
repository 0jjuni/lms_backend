from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Register, Submission
from .serializers import *
from rest_framework.permissions import BasePermission, SAFE_METHODS

from django.http import FileResponse
# Create your views here.

#교수 권한
class IsProfessor(BasePermission):
    message = '과제등록은 교수님만 가능합니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'P'

#다운로드 권한, P면 모두 가능, S면 자신이 작성한 글에 대해서만 가능
class IsMine(BasePermission):
    message = '파일 다운로드 권한이 없습니다.'

    def has_object_permission(self, request, view, obj):
        # 사용자 유형이 'P'인 경우 => 모두 가능
        if request.user.is_authenticated and request.user.user_type == 'P':
            return True
        # 사용자 유형이 'S'인 경우 => 자신이 작성한 글에 대해서만
        if request.user.is_authenticated and request.user.user_type == 'S':
            return obj.author == request.user
        return False

class InfoProfessor(BasePermission):
    message = "해당 작업은 교수님만 수행할 수 있습니다."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # POST나 PUT 요청일 경우 교수님만 접근 가능
        if request.method in ['POST', 'PUT']:
            return request.user.is_authenticated and request.user.user_type == 'P'
        return True
# 과제 등록
class RegisterCreateAPIView(generics.GenericAPIView):
    queryset = Register.objects.all()
    serializer_class = registerSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 과제글 정보, 삭제 예정
class RegisterInfo(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = registeInfoSerializer
    permission_classes = [IsAuthenticated, InfoProfessor]

#과제글 정보
class RegisterInfo2(generics.ListAPIView):
    serializer_class = registeInfoSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Register.objects.all()
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


# 과제글 수정
class RegisterUpdate(generics.UpdateAPIView):
    queryset = Register.objects.all()
    serializer_class = registerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# 과제글 삭제
class RegisterDelete(generics.DestroyAPIView):
    queryset = Register.objects.all()
    serializer_class = registerSerializer
    permission_classes = [IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))

        if obj.author != request.user:
            return Response({"권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

#과제제출(학생)

#과제제출
class SubmissionCreateAPIView(generics.GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = submissiontSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            assignment_id = serializer.validated_data.get('assignment').id
            assignment = Register.objects.get(id=assignment_id)
            # 과제 제출 기한 검사
            if assignment.due_date and assignment.due_date < timezone.now():
                return Response({"detail": "과제 제출 기한이 지났습니다."}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#제출게시글 Read
class SubmissionInfo(generics.ListAPIView):
    serializer_class = registeInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        assignment_id = self.request.query_params.get('assignment', None)
        if not assignment_id:
            raise serializers.ValidationError("Params에 assignment가 없습니다.")

        if user.user_type == 'P':
            return Submission.objects.filter(assignment_id=assignment_id)
        else:
            return Submission.objects.filter(author=user, assignment_id=assignment_id)

#과제제출수정
class SubmissionUpdate(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = submissionUpdateSerializer
    permission_classes = [IsAuthenticated]

    #사용자의 개시글만 접근 허용
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    # 사용자 권한 검증
    def get_object(self):
        obj = super().get_object()
        if obj.author != self.request.user:
            # 작성자와 사용자 다른 경우 403발생
            raise PermissionDenied('접근 권한이 없습니다.')
        return obj

    #제출게시글수정
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        # 과제 제출 기한 검사
        if instance.assignment.due_date and instance.assignment.due_date < timezone.now():
            raise ValidationError("과제 제출 기한이 지났습니다. 수정이 불가능합니다.")

        return self.partial_update(request, *args, **kwargs)





#제출게시글 삭제
class SubmissionDelete(generics.DestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = submissiontSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))

        # 사용자와 행위자 동일 확인 여부
        if obj.author != request.user:
            return Response({"detail": "삭제권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

#과제등록 파일 다운로드
class RegisterFileDownloadAPIView(generics.GenericAPIView):
    queryset = Register.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        register_instance = self.get_object()
        file_handle = register_instance.upload.path
        response = FileResponse(open(file_handle, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{register_instance.upload.name}"'
        return response

class SubmissionFileDownloadAPIView(generics.GenericAPIView):
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticated, IsMine]

    def get(self, request, *args, **kwargs):
        register_instance = self.get_object()
        file_handle = register_instance.upload.path
        response = FileResponse(open(file_handle, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{register_instance.upload.name}"'
        return response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/read/',
        '/update/<int:PK>',
        '/delete/<int:PK>',
        'download/<int:pk>/',
        '/info/',
        'submission_create/',
        "submission_read/",
        'submission_update/<int:PK>',
        'submission_delete/<int:PK>',
        'submission_download/<int:pk>/',
    ]
    return Response(routes)