from config.settings.base import *

# Speed up tests by choosing simple encryption for user passwords
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# CELERY_TASK_ALWAYS_EAGER = True  # execute tasks locally (no queuing)
# CELERY_TASK_EAGER_PROPAGATES = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}
