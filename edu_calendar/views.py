from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import PersonalCalendar
from .serializers import PersonalCalendarSerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.enrollment_number == request.user

class PersonalCalendarViewSet(viewsets.ModelViewSet):
    queryset = PersonalCalendar.objects.all()
    serializer_class = PersonalCalendarSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(enrollment_number=self.request.user)

    def perform_update(self, serializer, instance):
        serializer.save(enrollment_number=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return PersonalCalendar.objects.filter(enrollment_number=user)
