web: bin/runsvdir-dyno
worker: celery -A auction worker
beat: celery -A auction beat -S django
release: python manage.py migrate
