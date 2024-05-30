from .views import StudentEnrollmentList
from django.urls import path

urlpatterns = [
    path('enrollments/', StudentEnrollmentList.as_view(), name='student-enrollments'),
]