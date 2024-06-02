from django.shortcuts import render
from rest_framework import generics, status, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from django.db.models import Q
from .models import Question, Answer
from .serializers import QuestionSerializer, QuestionInfoSerializer, AnswerSerializer, AnswerInfoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
# Create your views here.

class IsProfessor(BasePermission):
    message = '답변은 교수님만 가능합니다.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'P'

#질문 등록

class QuestionCreateAPIView(generics.GenericAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionInfo(generics.ListAPIView):
    serializer_class = QuestionInfoSerializer
    permission_classes = [IsAuthenticated]

    #P는 모든 게시물, S는 공개 or 자신이 작성한 게시물
    def get_queryset(self):
        user = self.request.user
        queryset = Question.objects.all()

        #필터링
        author = self.request.query_params.get('author')
        title = self.request.query_params.get('title')
        subject_code = self.request.query_params.get('subject_code')

        if author:
            queryset = queryset.filter(author__username__icontains=author)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if subject_code:
            queryset = queryset.filter(subject_code=subject_code)
        #교수가 아닌 경우, 공개및 작성자만 보이도록 제작함.
        if user.user_type != 'P':
            queryset = queryset.filter(Q(status=0) | Q(author=user))

        return queryset


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
            return Response({"권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(obj)
        return Response({"삭제가 완료 되었습니다."},status=status.HTTP_204_NO_CONTENT)


#답변 생성
class AnswerCreateAPIView(generics.GenericAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#답변 READ기능 관련
class AnswerInfo(generics.ListAPIView):
    serializer_class = AnswerInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        question_id = self.request.query_params.get('question_id')
        if not question_id:
            raise serializers.ValidationError("Params에 question_id가 없습니다.")

        return Answer.objects.filter(question_id = question_id)

#답변 수정
class AnswerUpdate(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(author = self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
#답변 삭제
class AnswerDelete(generics.DestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))

        if obj.author != request.user:
            return Response({"권한이 없습니다."},
                            status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/create/',
        '/read/',
        '/update/<int:PK>',
        '/delete/<int:PK>',
        '/answer_create/',
        '/answer_read/',
        'answer_update/<int:PK>/',
        'answer_delete/<int:PK>/',
    ]
    return Response(routes)