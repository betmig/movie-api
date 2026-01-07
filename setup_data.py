#!/usr/bin/env python
"""
Complete data setup: Download CSV and import into database.
"""
import urllib.request
import os
import sys
import django

def download_csv():
    """Download the IMDB dataset."""
    url = "https://raw.githubusercontent.com/peetck/IMDB-Top1000-Movies/master/IMDB-Movie-Data.csv"
    output_file = "imdb_full.csv"

    print("Step 1: Downloading IMDB dataset...")
    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"✓ Downloaded to {output_file}\n")
        return True
    except Exception as e:
        print(f"✗ Error downloading: {e}\n")
        return False

def import_data():
    """Import the CSV data into database."""
    print("Step 2: Importing data into database...")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_api.settings')
    django.setup()

    from movies.models import Movie
    import csv

    csv_file = 'imdb_full.csv'
    if not os.path.exists(csv_file):
        print(f"✗ CSV file not found: {csv_file}")
        return False

    Movie.objects.all().delete()
    movies_created = 0

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                title = row['Title'].strip()
                director = row['Director'].strip() if row['Director'] else 'Unknown'
                genre = row['Genre'].strip()
                year = int(row['Year'])
                rating = float(row['Rating'])

                revenue = row.get('Revenue (Millions)', '').strip()
                budget = None
                if revenue and revenue != 'nan':
                    try:
                        budget = int(float(revenue) * 1000000)
                    except (ValueError, TypeError):
                        pass

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
                    print(f"  Imported {movies_created} movies...")

            except (ValueError, KeyError):
                continue

    print(f"✓ Imported {movies_created} movies\n")
    return True

if __name__ == '__main__':
    print("="*60)
    print("IMDB Movie Data Setup")
    print("="*60 + "\n")

    if download_csv() and import_data():
        print("="*60)
        print("✓ Setup complete!")
        print("="*60)
        print("\nYou can now:")
        print("  - Run the server: python manage.py runserver")
        print("  - Test the API: http://localhost:8000/api/docs/")
        print("  - View in admin: http://localhost:8000/admin/")
        sys.exit(0)
    else:
        print("="*60)
        print("✗ Setup failed")
        print("="*60)
        sys.exit(1)
