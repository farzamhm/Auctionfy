web: waitress-serve --port=$PORT {auction}.wsgi:application --log-file -
worker: celery -A auction worker
beat: celery -A auction beat -S django
release: python manage.py migrate
