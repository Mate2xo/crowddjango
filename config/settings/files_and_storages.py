from django.core.handlers.asgi import tempfile
from config.env import BASE_DIR, env

environment = env('DJANGO_SETTINGS_MODULE')
if environment == 'config.django.local':
    MEDIA_ROOT_NAME = 'media'
    MEDIA_ROOT = BASE_DIR / MEDIA_ROOT_NAME
    MEDIA_URL = f'/{MEDIA_ROOT_NAME}/'
elif environment == 'config.django.test':  # auto-clean uploaded test files
    MEDIA_ROOT_NAME = 'django_test_runs_media'
    MEDIA_ROOT = f"{tempfile.gettempdir()}/{MEDIA_ROOT_NAME}"
    MEDIA_URL = f'/{MEDIA_ROOT_NAME}/'
elif environment == 'config.django.staging' or environment == 'config.django.production':
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
