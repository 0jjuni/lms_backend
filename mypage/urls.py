from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeworkListViewSet, AnnouncementListViewSet

router = DefaultRouter()
router.register(r'homework', HomeworkListViewSet, basename='homework')
router.register(r'announcements', AnnouncementListViewSet, basename='announcements')

urlpatterns = [
    path('', include(router.urls)),
]