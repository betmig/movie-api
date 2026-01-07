"""
Comprehensive test suite for Movie API endpoints.
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Movie


class MovieAPITestCase(APITestCase):
    """
    Test cases for Movie API endpoints.
    """

    def setUp(self):
        """
        Set up test data before each test.
        """
        # Create test movies
        self.movie1 = Movie.objects.create(
            title="The Shawshank Redemption",
            director="Frank Darabont",
            genre="Drama",
            year=1994,
            rating=9.3,
            budget=25000000
        )
        self.movie2 = Movie.objects.create(
            title="The Godfather",
            director="Francis Ford Coppola",
            genre="Crime",
            year=1972,
            rating=9.2,
            budget=6000000
        )
        self.movie3 = Movie.objects.create(
            title="The Dark Knight",
            director="Christopher Nolan",
            genre="Action",
            year=2008,
            rating=9.0,
            budget=185000000
        )
        self.movie4 = Movie.objects.create(
            title="Pulp Fiction",
            director="Quentin Tarantino",
            genre="Crime",
            year=1994,
            rating=8.9,
            budget=8000000
        )
        self.movie5 = Movie.objects.create(
            title="Forrest Gump",
            director="Robert Zemeckis",
            genre="Drama",
            year=1994,
            rating=8.8,
            budget=55000000
        )

    def test_list_movies(self):
        """
        Test GET /api/movies/ returns list of movies.
        """
        url = reverse('movie-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)

    def test_retrieve_movie(self):
        """
        Test GET /api/movies/{id}/ returns single movie.
        """
        url = reverse('movie-detail', kwargs={'pk': self.movie1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "The Shawshank Redemption")
        self.assertEqual(response.data['director'], "Frank Darabont")
        self.assertEqual(response.data['rating'], 9.3)

    def test_create_movie_valid(self):
        """
        Test POST /api/movies/ with valid data returns 201.
        """
        url = reverse('movie-list')
        data = {
            'title': 'Inception',
            'director': 'Christopher Nolan',
            'genre': 'Sci-Fi',
            'year': 2010,
            'rating': 8.8,
            'budget': 160000000
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 6)
        self.assertEqual(response.data['title'], 'Inception')

    def test_create_movie_invalid_rating(self):
        """
        Test POST with rating > 10 returns 400.
        """
        url = reverse('movie-list')
        data = {
            'title': 'Test Movie',
            'director': 'Test Director',
            'genre': 'Test',
            'year': 2020,
            'rating': 11.0,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('rating', response.data)

    def test_create_movie_invalid_year(self):
        """
        Test POST with year < 1800 returns 400.
        """
        url = reverse('movie-list')
        data = {
            'title': 'Test Movie',
            'director': 'Test Director',
            'genre': 'Test',
            'year': 1700,
            'rating': 8.0,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', response.data)

    def test_update_movie(self):
        """
        Test PUT request updates movie correctly.
        """
        url = reverse('movie-detail', kwargs={'pk': self.movie1.pk})
        data = {
            'title': 'The Shawshank Redemption',
            'director': 'Frank Darabont',
            'genre': 'Drama',
            'year': 1994,
            'rating': 9.5,
            'budget': 25000000
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie1.refresh_from_db()
        self.assertEqual(self.movie1.rating, 9.5)

    def test_partial_update_movie(self):
        """
        Test PATCH request partially updates movie.
        """
        url = reverse('movie-detail', kwargs={'pk': self.movie2.pk})
        data = {'rating': 9.5}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie2.refresh_from_db()
        self.assertEqual(self.movie2.rating, 9.5)
        self.assertEqual(self.movie2.title, "The Godfather")

    def test_delete_movie(self):
        """
        Test DELETE returns 204 and removes movie.
        """
        url = reverse('movie-detail', kwargs={'pk': self.movie3.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movie.objects.count(), 4)
        self.assertFalse(Movie.objects.filter(pk=self.movie3.pk).exists())

    def test_top_rated_endpoint(self):
        """
        Test GET /api/movies/top-rated/ works.
        """
        url = reverse('movie-top-rated')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_top_rated_filter_by_rating(self):
        """
        Test query param min_rating=9 filters correctly.
        """
        url = reverse('movie-top-rated')
        response = self.client.get(url, {'min_rating': 9.0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 3)
        for movie in results:
            self.assertGreaterEqual(movie['rating'], 9.0)

    def test_top_rated_filter_by_genre(self):
        """
        Test query param genre filters correctly.
        """
        url = reverse('movie-top-rated')
        response = self.client.get(url, {'genre': 'Crime', 'min_rating': 8.0})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 2)
        for movie in results:
            self.assertEqual(movie['genre'].lower(), 'crime'.lower())

    def test_pagination(self):
        """
        Test list view includes pagination links.
        """
        url = reverse('movie-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    def test_retrieve_nonexistent_movie(self):
        """
        Test GET request for non-existent movie returns 404.
        """
        url = reverse('movie-detail', kwargs={'pk': 9999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_movie_missing_required_field(self):
        """
        Test POST without required field returns 400.
        """
        url = reverse('movie-list')
        data = {
            'director': 'Test Director',
            'genre': 'Test',
            'year': 2020,
            'rating': 8.0,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
