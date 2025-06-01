from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'blogs', BlogList, basename='blog')

urlpatterns = [
    path('categories/', CategoryListView.as_view()), # category ko list view
    path('categories/<int:pk>/', CategoryDetailView.as_view()), # category ko detail view
    path('blogs/', BlogList.as_view()), # blog ko list view
    path('blogs/<int:pk>/',BlogDetailView.as_view()), # blog ko detail view
    path('comments/', CommentList.as_view()), # comment ko list view
    path('comments/<int:pk>/', CommentDetailView.as_view()), # comment ko detail view
    
]