from django.urls import path, include
from .views import *
from announcement import views
urlpatterns = [
    path('', views.getRoutes),
    path('create/', announcementCreateAPIView.as_view(), name ='announcement-create'),
    path('update/<int:pk>/', announcementUpdate.as_view(), name ='announcement-update'),
    path('delete/<int:pk>/', annoucementDelete.as_view(), name ='announcement-delete'),

]