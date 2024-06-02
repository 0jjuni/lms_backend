from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalCalendarViewSet,HomeworkListViewSet

router = DefaultRouter()
router.register(r'persnal', PersonalCalendarViewSet)
router.register(r'homework', HomeworkListViewSet, basename='homework')

urlpatterns = [
    path('', include(router.urls)),
]