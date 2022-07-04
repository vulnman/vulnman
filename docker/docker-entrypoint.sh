#!/bin/bash

if [[ ! -f "vulnman/conf/local_settings.py" ]]; then
    cp docker/local_settings.template.py vulnman/conf/local_settings.py
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

echo "Update vulnerability templates"
python manage.py update_vulnerability_templates

echo "Update checklists"
python manage.py update_checklists

if [[ ! -f "vulnman/conf/secret_key.py" ]]; then
  python manage.py create_secret_key
fi

# create superuser
echo "Create superuser"
python manage.py createsuperuser --noinput

# Start server
echo "Starting server"
gunicorn --bind 0.0.0.0:8000 vulnman.wsgi