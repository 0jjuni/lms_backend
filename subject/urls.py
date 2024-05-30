from .views import StudentEnrollmentList
from django.urls import path
from . import views
urlpatterns = [
    path('enrollments/', StudentEnrollmentList.as_view(), name='student-enrollments'),
    path('', views.getRoutes),
]