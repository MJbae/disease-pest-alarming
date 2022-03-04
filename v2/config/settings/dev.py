from config.settings.common import *

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE = [
                 "debug_toolbar.middleware.DebugToolbarMiddleware",
             ] + MIDDLEWARE

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
