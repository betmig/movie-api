from django.shortcuts import render
from django.http import HttpResponse
from movies.models import Movie
import sys
import django
import rest_framework


def api_home(request):
    """
    Beautiful landing page for the Movie API.
    Displays system information, admin credentials, and API endpoints.
    """
    context = {
        'total_movies': Movie.objects.count(),
        'highest_rated': Movie.objects.order_by('-rating').first(),
        'latest_movie': Movie.objects.order_by('-year').first(),
        'oldest_movie': Movie.objects.order_by('year').first(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'django_version': django.get_version(),
        'drf_version': rest_framework.__version__,
    }
    return render(request, 'api_home.html', context)
