from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.getRoutes),
    path('create', NoticeBoardCreateAPIView.as_view(), name = 'create_board'),

]