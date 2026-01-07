"""
Django management command to import IMDB Top 1000 Movies data.
"""
import csv
import os
from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = 'Import IMDB Top 1000 Movies from CSV file'

    def handle(self, *args, **options):
        csv_file = 'imdb_full.csv'

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f'Error: {csv_file} not found!'))
            return

        self.stdout.write('Clearing existing movies...')
        Movie.objects.all().delete()

        self.stdout.write(f'Reading {csv_file}...')
        movies_created = 0
        movies_skipped = 0

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
                            budget = None

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
                        self.stdout.write(f'Imported {movies_created} movies...')

                except (ValueError, KeyError) as e:
                    movies_skipped += 1
                    self.stdout.write(
                        self.style.WARNING(f'Skipped row due to error: {e}')
                    )
                    continue

        self.stdout.write(self.style.SUCCESS(f'\n✓ Import complete!'))
        self.stdout.write(f'  - Movies created: {movies_created}')
        self.stdout.write(f'  - Movies skipped: {movies_skipped}')
        self.stdout.write(f'  - Total in database: {Movie.objects.count()}')
