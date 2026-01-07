#!/usr/bin/env python
"""
Script to load movie data from CSV file into the database.

Usage:
    python load_data.py

Expected CSV formats:
    Format 1: title,director,genre,year,rating,budget
    Format 2 (IMDB): Title,Genre,Director,Year,Rating,Revenue (Millions)

Data Source:
    The included movies.csv contains data from IMDB Top 1000 Movies.
    Source: https://raw.githubusercontent.com/peetck/IMDB-Top1000-Movies/master/IMDB-Movie-Data.csv
    Credit: Dataset by peetck on GitHub
"""
import os
import sys
import csv
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_api.settings')
django.setup()

from movies.models import Movie


def load_movies_from_csv(csv_file='imdb_full.csv'):
    """
    Load movies from CSV file into database.
    Supports both simple format and full IMDB format.

    Args:
        csv_file: Path to CSV file (default: imdb_full.csv)
    """
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        print("Please ensure the CSV file exists in the project root directory.")
        return

    created_count = 0
    updated_count = 0
    error_count = 0

    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Detect CSV format
            fieldnames = reader.fieldnames
            is_imdb_format = 'Title' in fieldnames and 'Director' in fieldnames
            is_simple_format = 'title' in fieldnames and 'director' in fieldnames

            if not is_imdb_format and not is_simple_format:
                print(f"Error: Unrecognized CSV format.")
                print(f"Columns found: {', '.join(fieldnames)}")
                return

            format_name = "IMDB" if is_imdb_format else "Simple"
            print(f"Loading movies from {csv_file} ({format_name} format)...")

            for row_num, row in enumerate(reader, start=2):
                try:
                    # Prepare movie data based on format
                    if is_imdb_format:
                        title = row['Title'].strip()
                        director = row['Director'].strip()
                        genre = row['Genre'].strip()
                        year = int(row['Year'])
                        rating = float(row['Rating'])

                        # Handle revenue as budget
                        budget = None
                        if 'Revenue (Millions)' in row and row['Revenue (Millions)']:
                            try:
                                # Convert millions to actual amount
                                budget = int(float(row['Revenue (Millions)']) * 1_000_000)
                            except (ValueError, TypeError):
                                pass
                    else:
                        title = row['title'].strip()
                        director = row['director'].strip()
                        genre = row['genre'].strip()
                        year = int(row['year'])
                        rating = float(row['rating'])

                        # Handle optional budget field
                        budget = None
                        if 'budget' in row and row['budget']:
                            try:
                                budget = int(row['budget'])
                            except (ValueError, TypeError):
                                pass

                    # Validate data
                    if not title or not director or not genre:
                        print(f"Row {row_num}: Skipping - empty required field")
                        error_count += 1
                        continue

                    if year < 1800 or year > 2100:
                        print(f"Row {row_num}: Skipping - invalid year {year}")
                        error_count += 1
                        continue

                    if rating < 0 or rating > 10:
                        print(f"Row {row_num}: Skipping - invalid rating {rating}")
                        error_count += 1
                        continue

                    # Create or update movie
                    movie, created = Movie.objects.get_or_create(
                        title=title,
                        year=year,
                        defaults={
                            'director': director,
                            'genre': genre,
                            'rating': rating,
                            'budget': budget
                        }
                    )

                    if created:
                        created_count += 1
                        print(f"Created: {title} ({year})")
                    else:
                        # Update existing movie
                        movie.director = director
                        movie.genre = genre
                        movie.rating = rating
                        movie.budget = budget
                        movie.save()
                        updated_count += 1
                        print(f"Updated: {title} ({year})")

                except (ValueError, KeyError) as e:
                    print(f"Row {row_num}: Error processing - {e}")
                    error_count += 1
                    continue

            # Print summary
            print("\n" + "="*50)
            print("Data Loading Summary")
            print("="*50)
            print(f"Movies created: {created_count}")
            print(f"Movies updated: {updated_count}")
            print(f"Errors: {error_count}")
            print(f"Total processed: {created_count + updated_count + error_count}")
            print("="*50)

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    load_movies_from_csv()
