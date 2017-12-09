worker: celery -A auction worker
beat: celery -A auction beat -S django
web: daphne auction.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
