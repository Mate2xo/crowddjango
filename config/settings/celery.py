from config.env import env

# https://docs.celeryproject.org/en/stable/userguide/configuration.html
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')

CELERY_TIMEZONE = 'Europe/Paris'

FLOWER_BASIC_AUTH = env('FLOWER_BASIC_AUTH')
# CELERY_TASK_SOFT_TIME_LIMIT = 20  # seconds
# CELERY_TASK_TIME_LIMIT = 30  # seconds
