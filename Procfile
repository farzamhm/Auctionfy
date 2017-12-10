web: gunicorn auction.wsgi --log-file -
web: node server.js
worker: celery -A auction worker
beat: celery -A auction beat -S django
release: python manage.py migrate
