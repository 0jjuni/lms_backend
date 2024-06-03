from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeworkListViewSet, AnnouncementListViewSet, QuestionListViewSet

router = DefaultRouter()
router.register(r'homework', HomeworkListViewSet, basename='homework')
router.register(r'announcements', AnnouncementListViewSet, basename='announcements')
router.register(r'questions', QuestionListViewSet, basename='questions')

urlpatterns = [
    path('', include(router.urls)),
]