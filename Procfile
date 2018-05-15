web: gunicorn config.wsgi:application
worker: celery worker --app=rural_norte.taskapp --loglevel=info
