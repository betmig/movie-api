"""
URL routing for movies app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet

# Create router and register viewset
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
]
