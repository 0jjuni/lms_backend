from django.urls import path, include
from .views import *
from lecture import views
urlpatterns = [
    path('', views.getRoutes),
    path('create/', lectureCreateAPIView.as_view(), name ='lecture-create'),
    path('read/', LectureInfo.as_view(), name ='lecture-create'),
    path('update/<int:pk>/', LectureUpdate.as_view(), name ='lecture-update'),
    path('delete/<int:pk>/', LectureDelete.as_view(), name ='lecture-delete'),

]