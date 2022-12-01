from config.env import env

from config.settings.base import *

ADMINS = env.list('ADMINS', default=[])
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env('EMAIL_PORT')
