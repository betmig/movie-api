"""
Import IMDB Top 1000 Movies data into the database.
"""
import os
import sys
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_api.settings')
django.setup()

from movies.models import Movie

def import_movies():
    """Import movies from IMDB CSV file."""
    csv_file = 'imdb_full.csv'

    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return

    # Clear existing movies
    print("Clearing existing movies...")
    Movie.objects.all().delete()

    # Read and import CSV
    print(f"Reading {csv_file}...")
    movies_created = 0
    movies_skipped = 0

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                # Extract data from CSV
                title = row['Title'].strip()
                director = row['Director'].strip() if row['Director'] else 'Unknown'
                genre = row['Genre'].strip()
                year = int(row['Year'])
                rating = float(row['Rating'])

                # Handle Revenue (Millions) - convert to budget equivalent
                revenue = row.get('Revenue (Millions)', '').strip()
                budget = None
                if revenue and revenue != 'nan':
                    try:
                        # Convert millions to actual amount
                        budget = int(float(revenue) * 1000000)
                    except (ValueError, TypeError):
                        budget = None

                # Create movie
                Movie.objects.create(
                    title=title,
                    director=director,
                    genre=genre,
                    year=year,
                    rating=rating,
                    budget=budget
                )
                movies_created += 1

                if movies_created % 100 == 0:
                    print(f"Imported {movies_created} movies...")

            except (ValueError, KeyError) as e:
                movies_skipped += 1
                print(f"Skipped row due to error: {e}")
                continue

    print(f"\n✓ Import complete!")
    print(f"  - Movies created: {movies_created}")
    print(f"  - Movies skipped: {movies_skipped}")
    print(f"  - Total in database: {Movie.objects.count()}")

if __name__ == '__main__':
    import_movies()
