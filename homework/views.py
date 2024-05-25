from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Register, Submission
from .serializers import *

# Create your views here.
# 과제 등록
class registerCreateAPIView(generics.GenericAPIView):
    queryset = Register
    serializer_class = registerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request,*args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 과제글 정보
class registerInfo(viewsets.ModelViewSet):
    queryset = Register.objects.all()
    serializer_class = registeInfoSerializer

# 과제글 수정
class registerUpdate(generics.UpdateAPIView):
    queryset = Register.objects.all()
    serializer_class = registerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# 과제글 수정 구버전
    # def put(self, request, *args, **kwargs):
    #     obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
    #     # 작성자와 수정자 일치여부 확인
    #     if obj.author != request.user:
    #         return  Response({"detail": "권한이 없습니다.(자신이 작성한 글만 수정이 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
    #     serializer = self.get_serializer(obj, data=request.data, partial=False)  # Update the entire instance
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 과제글 삭제
class RegisterDelete(generics.DestroyAPIView):
    queryset = Register.objects.all()
    serializer_class = registerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))

        # 사용자와 행위자 동일 확인 여부
        if obj.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

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

#과제제출수정
class submissionUpdate(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = submissionUpdateSerializer
    permission_classes = [IsAuthenticated]

    #사용자의 개시글만 접근 허용
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)
    #제출게시글수정
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

#과제글 삭제
class submissionDelete(generics.DestroyAPIView):
    queryset = Submission.objects.all()
    serializer_class = submissiontSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))

        # 사용자와 행위자 동일 확인 여부
        if obj.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/update/<int:PK>',
        '/delete/<int:PK>',
        '/info/',
        'submission_create/',
        'submission_update/<int:PK>',
        'submission_delete/<int:PK>',
    ]
    return Response(routes)