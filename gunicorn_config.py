bind = "127.0.0.1:8000"
bind = 'unix:app.sock'


# workers = (2 * cpu) + 1

timeout = 120
keepalive = 2

# this is needed to get access log in django logger.
accesslog = '/path/to/your/gunicorn_access.log'
errorlog = '/path/to/your/gunicorn_error.log'
loglevel = 'info'


# gunicorn -c /path/to/your/gunicorn_config.py your_app_module.wsgi:application
