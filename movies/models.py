"""
Movie model with field validation.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Movie(models.Model):
    """
    Movie model representing a film with its metadata.

    Fields:
        title: Movie title (required)
        director: Director name (required)
        genre: Movie genre (required)
        year: Release year (1800-2100)
        rating: Movie rating (0-10)
        budget: Production budget (optional)
        created_at: Timestamp of record creation
    """
    title = models.CharField(
        max_length=200,
        help_text="Movie title"
    )
    director = models.CharField(
        max_length=100,
        help_text="Director name"
    )
    genre = models.CharField(
        max_length=100,
        help_text="Movie genre"
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(1800, message="Year must be at least 1800"),
            MaxValueValidator(2100, message="Year cannot exceed 2100")
        ],
        help_text="Release year (1800-2100)"
    )
    rating = models.FloatField(
        validators=[
            MinValueValidator(0.0, message="Rating must be at least 0"),
            MaxValueValidator(10.0, message="Rating cannot exceed 10")
        ],
        help_text="Movie rating (0-10)"
    )
    budget = models.IntegerField(
        null=True,
        blank=True,
        help_text="Production budget (optional)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Record creation timestamp"
    )

    class Meta:
        ordering = ['-year', '-rating']
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return f"{self.title} ({self.year})"
