from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonalCalendarViewSet

router = DefaultRouter()
router.register(r'', PersonalCalendarViewSet)

urlpatterns = [
    path('', include(router.urls)),
]