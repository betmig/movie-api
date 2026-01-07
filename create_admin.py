#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_api.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f"Admin user '{username}' already exists")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"Password updated for '{username}'")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully")
    print(f"Username: {username}")
    print(f"Password: {password}")
