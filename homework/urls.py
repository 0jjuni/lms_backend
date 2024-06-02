from django.urls import path,include
from .views import *
from homework import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'register-info', RegisterInfo)


urlpatterns = [
    path('', views.getRoutes),
    path('create/', RegisterCreateAPIView.as_view(), name = 'register_homework'),
    path('read/', RegisterInfo2.as_view(), name='register_read'),
    path('update/<int:pk>/', RegisterUpdate.as_view(), name = 'register_upadte'),
    path('delete/<int:pk>/', RegisterDelete.as_view(), name='register_delete'),
    path('download/<int:pk>/', RegisterFileDownloadAPIView.as_view(), name='register_download'),
    path('submission_create/', SubmissionCreateAPIView.as_view(), name='submission-create'),
    path('submission_read/', SubmissionInfo.as_view(), name='submission-create'),
    path('submission_update/<int:pk>/', SubmissionUpdate.as_view(), name = 'submission_upadte'),
    path('submission_delete/<int:pk>/', SubmissionDelete.as_view(), name = 'submission_delete'),
    path('submission_download/<int:pk>/', SubmissionFileDownloadAPIView.as_view(), name = 'submission_delete'),
    path('info/', include(router.urls), name = "register_info") #삭제예정
]