#!/bin/bash

# Exit on error
set -e

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# (Optional) Create a superuser for the app (if needed)
python manage.py createsuperuser --noinput --username admin --email admin@example.com
