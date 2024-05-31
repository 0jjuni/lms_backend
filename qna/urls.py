from django.urls import path,include
from .views import *
from qna import views


urlpatterns = [
    path('', views.getRoutes),
    path('create/', QuestionCreateAPIView.as_view(), name = 'Question_create'),
    path('read/', QuestionInfo.as_view(), name = 'Question_read'),
    path('update/<int:pk>/', QuestionUpdate.as_view(), name='question_update'),
    path('delete/<int:pk>/', QuestionDelete.as_view(), name='question_delete'),
    path('answer_create/', AnswerCreateAPIView.as_view(), name='Answer-create'),
    path('answer_read/', AnswerInfo.as_view(), name='Answer-read'),
    path('answer_update/<int:pk>/', AnswerUpdate.as_view(), name='Answer-update'),
    path('answer_delete/<int:pk>/', AnswerDelete.as_view(), name='Answer-delte'),


]