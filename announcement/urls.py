from django.urls import path, include
from .views import *
from announcement import views
urlpatterns = [
    path('', views.getRoutes),
    path('create/', AnnouncementCreateAPIView.as_view(), name ='announcement-create'),
    path('read/', AnnouncementInfo.as_view(), name ='announcement-create'),
    path('update/<int:pk>/', AnnouncementUpdate.as_view(), name ='announcement-update'),
    path('delete/<int:pk>/', AnnoucementDelete.as_view(), name ='announcement-delete'),

]