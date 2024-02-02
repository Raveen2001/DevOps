import os


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s - %(asctime)s - %(name)s %(filename)s.%(funcName)s:%(lineno)s - %(message)s \n-------------\n'
        },
    },
    'handlers': {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f'{os.path.expanduser("~")}/logs/debug.log',
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'propagate': True,
        },
        'gunicorn.access': {
            'propagate': True,
        },
        "root": {
            "handlers": ["file"],
            "level": "INFO",
        },
    },
}
