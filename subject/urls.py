from .views import StudentEnrollmentList, ProfessorSubjectList
from django.urls import path
from . import views


urlpatterns = [
    path('enrollments/', StudentEnrollmentList.as_view(), name='student-enrollments'),
    path('info/', ProfessorSubjectList.as_view(), name='professor-subjects'),
    path('', views.getRoutes),
]