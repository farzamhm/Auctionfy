web: gunicorn auction.wsgi --log-file -
worker: celery -A auction worker -B --loglevel=info
beat: celery -A auction beat -S django
release: python manage.py migrate
