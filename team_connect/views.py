from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import *
from .serializers import *
# Create your views here.

# 팀원모집글 작성
class ConnectCreateAPIView(generics.GenericAPIView):
    queryset = Connect.objects.all()
    serializer_class = ConnectSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#팀원모집글 수정
class ConnectUpdate(generics.UpdateAPIView):
    queryset = Connect.objects.all()
    serializer_class = ConnectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        filtered_queryset = queryset.filter(author=self.request.user)
        if not filtered_queryset.exists():
            raise PermissionDenied("수정권한이 없습니다.")
        return filtered_queryset



#팀원모집글 삭제
class ConnectDelete(generics.DestroyAPIView):
    queryset = Connect.objects.all()
    serializer_class = ConnectSerializer
    permission_classes = [IsAuthenticated]

    # 사용자와 행위자 동일 확인 여부
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        user_queryset = self.get_queryset()
        if not user_queryset.exists():
            raise ValidationError("권한이 없습니다.")

        obj = get_object_or_404(user_queryset, pk=kwargs.get('pk'))

        self.perform_destroy(obj)
        return Response({"삭제가 완료 되었습니다."}, status=status.HTTP_204_NO_CONTENT)

#팀원 모집글 Read
class ConnectInfo(generics.ListAPIView):
    serializer_class = ConnectSerializer
    permission_classes = [IsAuthenticated]

    #P는 모든 게시물, S는 공개 or 자신이 작성한 게시물
    def get_queryset(self):
        user = self.request.user
        queryset = Connect.objects.all()

        #필터링
        author = self.request.query_params.get('author')
        title = self.request.query_params.get('title')
        subject_code = self.request.query_params.get('subject_code')
        status = self.request.query_params.get('status')

        if author:
            queryset = queryset.filter(author__username__icontains=author)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if subject_code:
            queryset = queryset.filter(subject_code=subject_code)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


#팀원모집글 신청서 작성_댓글 형식
class ConnectAnswerCreateAPIView(generics.GenericAPIView):
    queryset = Connect_answer.objects.all()
    serializer_class = ConnectAnswerSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            connect = serializer.validated_data.get("connect")
            if connect.status == 1:
                return Response({"detail": "모집 완료된 글에는 답변을 작성할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#팀원모집글 신청서 수정
class ConnectAnswerUpdate(generics.UpdateAPIView):
    queryset = Connect_answer.objects.all()
    serializer_class = ConnectAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("수정 권한이 없습니다.")
        serializer.save()

#팀원모집글 신청서 read_댓글형식
class ConnectAnswerInfo(generics.ListAPIView):
    serializer_class = ConnectAnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        connect = self.request.query_params.get('connect')
        if not connect:
            raise serializers.ValidationError("Params에 connect가 없습니다.")

        return Connect_answer.objects.filter(connect = connect)

#팀원모집글 신청서 삭제
class ConnectAnswerDelete(generics.DestroyAPIView):
    queryset = Connect_answer.objects.all()
    serializer_class = ConnectAnswerSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))

        # 사용자와 행위자 동일 확인 여부
        if obj.author != request.user:
            return Response({"권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(obj)
        return Response({"삭제가 완료 되었습니다."}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/read/',
        '/update/<int:PK>',
        '/delete/<int:PK>',
        '/Connect_answer_create/',
        '/Connect_answer_read/',
        '/Connect_answer_update/<int:PK>/',
        '/Connect_answer_delete/<int:PK>/',
    ]
    return Response(routes)