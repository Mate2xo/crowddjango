from .base import *

DEBUG = False

# Speed up tests by choosing simple encryption for user passwords
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# CELERY_BROKER_BACKEND = "memory"
# CELERY_TASK_ALWAYS_EAGER = True
# CELERY_TASK_EAGER_PROPAGATES = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
