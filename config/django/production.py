from config.env import env

from .base import *

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
