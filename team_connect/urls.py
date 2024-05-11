# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.TeamRecruitmentCreateAPIView.as_view(), name='team-recruitment-create'),
    path('update/<int:pk>/', views.TeamRecruitmentUpdateAPIView.as_view(), name='team-recruitment-update'),
    path('', views.getRoutes, name='get-routes'),
    path('search_by_title/', views.TeamRecruitmentViewSet.as_view({'post': 'search_by_title'}), name='team-recruitment-search-by-title')
]