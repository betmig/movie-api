"""
ViewSet for Movie API endpoints.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Movie
from .serializers import MovieSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all movies",
        description="Retrieve a paginated list of all movies in the database. Returns 20 movies per page.",
        tags=["Movies"],
    ),
    retrieve=extend_schema(
        summary="Get movie by ID",
        description="Retrieve detailed information about a specific movie.",
        tags=["Movies"],
    ),
    create=extend_schema(
        summary="Create new movie",
        description="Add a new movie to the database. All fields except budget are required.",
        tags=["Movies"],
        examples=[
            OpenApiExample(
                'Create Action Movie',
                value={
                    "title": "Inception",
                    "director": "Christopher Nolan",
                    "genre": "Sci-Fi",
                    "year": 2010,
                    "rating": 8.8,
                    "budget": 160000000
                },
                request_only=True,
            ),
        ],
    ),
    update=extend_schema(
        summary="Update entire movie",
        description="Update all fields of an existing movie. All required fields must be provided.",
        tags=["Movies"],
    ),
    partial_update=extend_schema(
        summary="Partial movie update",
        description="Update one or more fields of an existing movie. Only provided fields will be updated.",
        tags=["Movies"],
        examples=[
            OpenApiExample(
                'Update Rating',
                value={"rating": 9.5},
                request_only=True,
            ),
        ],
    ),
    destroy=extend_schema(
        summary="Delete movie",
        description="Remove a movie from the database permanently.",
        tags=["Movies"],
    ),
)
class MovieViewSet(viewsets.ModelViewSet):
    """
    Complete CRUD operations for movie management.

    This ViewSet provides standard endpoints for creating, reading, updating,
    and deleting movies, plus a custom endpoint for retrieving top-rated movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @extend_schema(
        summary="Get top-rated movies",
        description="Retrieve movies filtered by rating and optionally by genre and year. "
                    "Results are ordered by rating (descending), then year (descending).",
        tags=["Movies"],
        parameters=[
            OpenApiParameter(
                name='min_rating',
                type=OpenApiTypes.FLOAT,
                location=OpenApiParameter.QUERY,
                description='Minimum rating threshold (0-10)',
                required=False,
                default=8.0,
            ),
            OpenApiParameter(
                name='genre',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by genre (case-insensitive)',
                required=False,
                examples=[
                    OpenApiExample('Action', value='Action'),
                    OpenApiExample('Drama', value='Drama'),
                    OpenApiExample('Sci-Fi', value='Sci-Fi'),
                ],
            ),
            OpenApiParameter(
                name='year',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filter by release year',
                required=False,
            ),
        ],
        examples=[
            OpenApiExample(
                'Top Rated Response',
                value={
                    "count": 5,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "title": "The Shawshank Redemption",
                            "director": "Frank Darabont",
                            "genre": "Drama",
                            "year": 1994,
                            "rating": 9.3,
                            "budget": 25000000,
                            "created_at": "2026-01-03T12:00:00Z"
                        }
                    ]
                },
                response_only=True,
            ),
        ],
    )
    @action(detail=False, methods=['get'], url_path='top-rated')
    def top_rated(self, request):
        """
        Get top-rated movies with optional filters.
        """
        # Get query parameters with defaults
        min_rating = request.query_params.get('min_rating', 8.0)
        genre = request.query_params.get('genre', None)
        year = request.query_params.get('year', None)

        # Convert min_rating to float
        try:
            min_rating = float(min_rating)
        except (ValueError, TypeError):
            return Response(
                {'error': 'min_rating must be a valid number'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Start with base queryset filtered by rating
        queryset = Movie.objects.filter(rating__gte=min_rating)

        # Apply genre filter if provided (case-insensitive contains)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)

        # Apply year filter if provided
        if year:
            try:
                year = int(year)
                queryset = queryset.filter(year=year)
            except (ValueError, TypeError):
                return Response(
                    {'error': 'year must be a valid integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Order by rating (descending), then year (descending)
        queryset = queryset.order_by('-rating', '-year')

        # Paginate results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new movie with validation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        """
        Update a movie (full update).
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a movie.
        """
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a movie.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
