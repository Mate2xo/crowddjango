from config.settings.base import *

DEBUG = True
EMAIL_PORT = 1025  # send mails to local MailHog server
CELERY_BROKER_BACKEND = "memory"
