web: gunicorn ecommerce_api.wsgi --log-file - 
web: python manage.py migrate && gunicorn ecommerce_api.wsgi
