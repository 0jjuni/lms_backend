from django.urls import path,include
from .views import *
from homework import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'register-info', registerInfo)


urlpatterns = [
    path('', views.getRoutes),
    path('create/', registerCreateAPIView.as_view(), name = 'register_homework'),
    path('update/<int:pk>/', registerUpdate.as_view(), name = 'register_upadte'),
    path('delete/<int:pk>/', RegisterDelete.as_view(), name='register_delete'),
    path('submission_create/', submissionCreateAPIView.as_view(), name='submission-create'),
    path('info/', include(router.urls), name = "register_info")
]