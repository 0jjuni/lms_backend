from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Register, Submission
from .serializers import *

# Create your views here.

# 과제 등록
class registerCreateAPIView(generics.GenericAPIView):
    queryset = Register.objects.all()
    serializer_class = registerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 과제글 정보, 삭제 예정
class registerInfo(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = registeInfoSerializer

#과제글 정보
class registerInfo2(generics.ListAPIView):
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
class registerUpdate(generics.UpdateAPIView):
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
class submissionCreateAPIView(generics.GenericAPIView):
    queryset = Submission.objects.all()
    serializer_class = submissiontSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#제출게시글 Read
class submissionInfo(generics.ListAPIView):
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
class submissionUpdate(generics.UpdateAPIView):
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
        return self.partial_update(request, *args, **kwargs)





#제출게시글 삭제
class submissionDelete(generics.DestroyAPIView):
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

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        'read/',
        '/update/<int:PK>',
        '/delete/<int:PK>',
        '/info/',
        'submission_create/',
        "submission_read /",
        'submission_update/<int:PK>',
        'submission_delete/<int:PK>',
    ]
    return Response(routes)