from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import HomeworkSerializer
from homework.models import Register
from subject.models import Enrollment
from rest_framework.response import Response

# Create your views here.
class HomeworkListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        student = request.user.student
        enrollments = Enrollment.objects.filter(student=student)
        subject_codes = enrollments.values_list('subject__subject_code', flat=True)
        homeworks = Register.objects.filter(subject_code__in=subject_codes)
        serializer = HomeworkSerializer(homeworks, many=True)
        return Response(serializer.data)