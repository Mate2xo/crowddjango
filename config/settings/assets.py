# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
from config.env import BASE_DIR

STATIC_URL = 'static/'
MEDIA_ROOT_NAME = 'media'
MEDIA_ROOT = BASE_DIR / MEDIA_ROOT_NAME
MEDIA_URL = f'/{MEDIA_ROOT_NAME}/'
