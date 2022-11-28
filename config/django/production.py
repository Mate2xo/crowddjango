from config.env import env

from config.settings.base import *

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
