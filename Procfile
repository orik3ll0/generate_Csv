web: gunicorn planeks.wsgi
worker: celery -A planeks worker -l info --pool=solo