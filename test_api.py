#!/usr/bin/env python
"""
Simple script to test all Movie API endpoints.

This script demonstrates all CRUD operations and custom endpoints.
Run the Django server first: python manage.py runserver
Then run this script: python test_api.py
"""
import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000/api/movies/"


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_list_movies():
    """Test GET /api/movies/ - List all movies."""
    print_section("1. LIST ALL MOVIES")
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Total movies: {data['count']}")
    print(f"First 3 movies:")
    for movie in data['results'][:3]:
        print(f"  - {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")


def test_get_single_movie():
    """Test GET /api/movies/{id}/ - Get single movie."""
    print_section("2. GET SINGLE MOVIE")
    response = requests.get(f"{BASE_URL}1/")
    print(f"Status Code: {response.status_code}")
    movie = response.json()
    print(f"Movie Details:")
    print(f"  Title: {movie['title']}")
    print(f"  Director: {movie['director']}")
    print(f"  Genre: {movie['genre']}")
    print(f"  Year: {movie['year']}")
    print(f"  Rating: {movie['rating']}")


def test_create_movie():
    """Test POST /api/movies/ - Create new movie."""
    print_section("3. CREATE NEW MOVIE")
    new_movie = {
        "title": "Test Movie",
        "director": "Test Director",
        "genre": "Action",
        "year": 2023,
        "rating": 8.5,
        "budget": 100000000
    }
    response = requests.post(BASE_URL, json=new_movie)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 201:
        movie = response.json()
        print(f"Created movie ID: {movie['id']}")
        print(f"Title: {movie['title']}")
        return movie['id']
    return None


def test_update_movie(movie_id):
    """Test PUT /api/movies/{id}/ - Update entire movie."""
    print_section("4. UPDATE MOVIE (PUT)")
    updated_data = {
        "title": "Test Movie Updated",
        "director": "Test Director",
        "genre": "Drama",
        "year": 2023,
        "rating": 9.0,
        "budget": 100000000
    }
    response = requests.put(f"{BASE_URL}{movie_id}/", json=updated_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        movie = response.json()
        print(f"Updated title: {movie['title']}")
        print(f"Updated rating: {movie['rating']}")


def test_partial_update_movie(movie_id):
    """Test PATCH /api/movies/{id}/ - Partial update."""
    print_section("5. PARTIAL UPDATE (PATCH)")
    partial_data = {
        "rating": 9.5
    }
    response = requests.patch(f"{BASE_URL}{movie_id}/", json=partial_data)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        movie = response.json()
        print(f"Updated rating: {movie['rating']}")


def test_top_rated_default():
    """Test GET /api/movies/top-rated/ - Default filter."""
    print_section("6. TOP-RATED MOVIES (Default)")
    response = requests.get(f"{BASE_URL}top-rated/")
    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Movies with rating >= 8.0: {data['count']}")
    print(f"Top 3 movies:")
    for movie in data['results'][:3]:
        print(f"  - {movie['title']} ({movie['year']}) - Rating: {movie['rating']}")


def test_top_rated_with_filters():
    """Test GET /api/movies/top-rated/ with filters."""
    print_section("7. TOP-RATED MOVIES (With Filters)")

    # Test min_rating filter
    print("\nMovies with rating >= 9.0:")
    response = requests.get(f"{BASE_URL}top-rated/?min_rating=9.0")
    data = response.json()
    print(f"Count: {data['count']}")

    # Test genre filter
    print("\nCrime movies with rating >= 8.0:")
    response = requests.get(f"{BASE_URL}top-rated/?genre=Crime")
    data = response.json()
    print(f"Count: {data['count']}")
    if data['results']:
        print(f"Example: {data['results'][0]['title']}")

    # Test year filter
    print("\nMovies from 1994 with rating >= 8.0:")
    response = requests.get(f"{BASE_URL}top-rated/?year=1994")
    data = response.json()
    print(f"Count: {data['count']}")


def test_delete_movie(movie_id):
    """Test DELETE /api/movies/{id}/ - Delete movie."""
    print_section("8. DELETE MOVIE")
    response = requests.delete(f"{BASE_URL}{movie_id}/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 204:
        print(f"Movie {movie_id} deleted successfully")


def test_validation_errors():
    """Test validation with invalid data."""
    print_section("9. TEST VALIDATION")

    # Test invalid rating
    print("\nTest invalid rating (> 10):")
    invalid_movie = {
        "title": "Invalid Movie",
        "director": "Director",
        "genre": "Action",
        "year": 2023,
        "rating": 11.0
    }
    response = requests.post(BASE_URL, json=invalid_movie)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        print(f"Error: {response.json()}")

    # Test invalid year
    print("\nTest invalid year (< 1800):")
    invalid_movie["rating"] = 8.0
    invalid_movie["year"] = 1700
    response = requests.post(BASE_URL, json=invalid_movie)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 400:
        print(f"Error: {response.json()}")


def main():
    """Run all API tests."""
    print("\n" + "=" * 60)
    print("  DJANGO MOVIE API - ENDPOINT TESTING")
    print("=" * 60)
    print("\nMake sure the Django server is running:")
    print("  python manage.py runserver")
    print("\nTesting endpoints...")

    try:
        # Test read operations
        test_list_movies()
        test_get_single_movie()

        # Test create
        movie_id = test_create_movie()

        if movie_id:
            # Test updates
            test_update_movie(movie_id)
            test_partial_update_movie(movie_id)

        # Test custom endpoint
        test_top_rated_default()
        test_top_rated_with_filters()

        # Test validation
        test_validation_errors()

        # Test delete (cleanup)
        if movie_id:
            test_delete_movie(movie_id)

        print("\n" + "=" * 60)
        print("  ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Please make sure the Django server is running:")
        print("  python manage.py runserver")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()
