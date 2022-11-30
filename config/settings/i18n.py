from django.utils.translation import gettext_lazy as _

from config.env import BASE_DIR

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = 'FR-fr'
LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French'))
]
LOCALE_PATHS = [
    BASE_DIR / 'mysite' / 'locale',
]
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True
