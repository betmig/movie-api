"""
Admin configuration for Movie model.
"""
from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Movie model.
    """
    list_display = ['title', 'director', 'year', 'rating', 'genre']
    list_filter = ['year', 'genre', 'rating']
    search_fields = ['title', 'director']
    ordering = ['-year']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'director', 'genre')
        }),
        ('Details', {
            'fields': ('year', 'rating', 'budget')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at']
