from django.urls import path,include
from noticeboard import views
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'noticeboard', Noice_board_info)

urlpatterns = [
    path('', views.getRoutes),
    path('create/', NoticeBoardCreateAPIView.as_view(), name = 'create_board'),
    path('update/<int:pk>/', NoticeBoardUpdateAPIView.as_view(), name='noticeboard-update'),
    path('info/', include(router.urls), name = 'noticeboard_info'),

]