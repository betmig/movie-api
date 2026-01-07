"""
Serializers for Movie model with validation.
"""
from rest_framework import serializers
from .models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for Movie model with field validation.

    Validates:
        - Rating: 0-10 range
        - Year: 1800-2100 range
        - Required fields: title, director, genre
    """

    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'genre', 'year', 'rating', 'budget', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        """
        Validate rating is within 0-10 range.
        """
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                "Rating must be between 0 and 10."
            )
        return value

    def validate_year(self, value):
        """
        Validate year is within 1800-2100 range.
        """
        if value < 1800 or value > 2100:
            raise serializers.ValidationError(
                "Year must be between 1800 and 2100."
            )
        return value

    def validate_title(self, value):
        """
        Validate title is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty."
            )
        return value.strip()

    def validate_director(self, value):
        """
        Validate director is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Director cannot be empty."
            )
        return value.strip()

    def validate_genre(self, value):
        """
        Validate genre is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(
                "Genre cannot be empty."
            )
        return value.strip()
