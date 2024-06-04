from django.urls import path, include
from .views import *
from announcement import views
urlpatterns = [
    path('', views.getRoutes),
    path('create/', SyllabusCreateAPIView.as_view(), name ='Syllabus-create'),
    path('read/', TotalSyllabus.as_view(), name ='Syllabus-read'),
    path('update/<str:subject_code>/', SyllabusUpdate.as_view(), name='syllabus-update'),
    path('delete/<str:subject_code>/', SyllabusDelete.as_view(), name='syllabus-delete'),
]