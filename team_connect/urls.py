from django.urls import path,include
from .views import *
from team_connect import views


urlpatterns = [
    path('', views.getRoutes),
    path('create/', ConnectCreateAPIView.as_view(), name = 'Connect'),
    path('read/', ConnectInfo.as_view(), name = 'Connect_read'),
    path('update/<int:pk>/', ConnectUpdate.as_view(), name='Connect_update'),
    path('delete/<int:pk>/', ConnectDelete.as_view(), name='Connect_delete'),
    path('Connect_answer_create/', ConnectAnswerCreateAPIView.as_view(), name='Connect_answer_create'),
    path('Connect_answer_read/', ConnectAnswerInfo.as_view(), name='Connect_answer_read'),
    path('Connect_answer_update/<int:pk>/', ConnectAnswerUpdate.as_view(), name='Connect_answer_update'),
    path('Connect_answer_delete/<int:pk>/', ConnectAnswerDelete.as_view(), name='Connect_answer_delete'),


]