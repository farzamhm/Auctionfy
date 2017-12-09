 INSTALLED_APPS = [
 
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat' ,
    'django_celery_results' ,
    "main",
    
     ## your apps
 ]
 CELERY_BROKER_URL=os.environ['REDIS_URL']
 CELERY_RESULT_BACKEND=os.environ['REDIS_URL']

 CELERY_ACCEPT_CONTENT = ['application/json']
 CELERY_TASK_SERIALIZER = 'json'
 CELERY_RESULT_SERIALIZER = 'json'
 CELERY_TIMEZONE = TIME_ZONE