from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q

from .models import Question
from .serializers import QuestionSerializer, QuestionInfoSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

#질문 등록

class QuestionCreateAPIView(generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    # subject_code에 해당하는 학생만 작성할 수 있도록 수정 계획 세우기
    # def get_queryset(self):
    #     return self.queryset.filter(author = )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionInfoSerializer
    permission_classes = [IsAuthenticated]

    #P는 모든 게시물, S는 공개 or 자신이 작성한 게시물
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'P':
            return Question.objects.all()
        else:
            return Question.objects.filter(Q(status=0) | Q(author=user))
#질문 수정
class QuestionUpdate(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

#질문 삭제
class QuestionDelete(generics.DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    # 사용자와 행위자 동일 확인 여부
    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))

        # 사용자와 행위자 동일 확인 여부
        if obj.author != request.user:
            return Response({"detail": "You do not have permission to delete this post."},
                            status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/update/<int:PK>',
        '/delete/<int:PK>',
        '/questions/',
    ]
    return Response(routes)