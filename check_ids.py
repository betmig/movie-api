import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_api.settings')
django.setup()

from movies.models import Movie

movies = Movie.objects.all()[:10]
print("First 10 movie IDs:")
for m in movies:
    print(f"ID: {m.id}, Title: {m.title}")

print(f"\nTotal movies: {Movie.objects.count()}")
