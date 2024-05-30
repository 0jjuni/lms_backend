from django.urls import path,include
from .views import *
from qna import views


urlpatterns = [
    path('', views.getRoutes),
    path('create/', QuestionCreateAPIView.as_view(), name = 'Question_create'),
    path('read/', QuestionListView.as_view(), name = 'Question_create'),
    path('update/<int:pk>/', QuestionUpdate.as_view(), name='question_update'),
    path('delete/<int:pk>/', QuestionDelete.as_view(), name='question_delete'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('answer/', AnswerCreateAPIView.as_view(), name='Answer-create'),
    path('answer/update/<int:pk>/', AnswerUpdate.as_view(), name='Answer-update'),
    path('answer/delete/<int:pk>/', AnswerDelete.as_view(), name='Answer-delte'),


]