web: gunicorn auction.wsgi --log-file -
worker: celery -A auction worker
beat: celery -A auction beat -S django
release: python manage.py migrate
release: python manage.py createsuperuser
