web: gunicorn auction.wsgi --timeout 15 --keep-alive 5 --log-file -
worker: celery -A auction worker
beat: celery -A auction beat -S django
release: python manage.py migrate
