import os
import logging
from pathlib import Path

logger = logging.getLogger('django')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-t6*7!_0fg#@nimjj9f)*^ko*ox1p(8537dkiqi48+9u+nw0w@('

DEBUG = True

ALLOWED_HOSTS = []


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'accounts',
    'news',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'news.middlewares.TimezoneMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_REDIRECT_URL = "/"

ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'test@yandex.ru'
EMAIL_HOST_PASSWORD = 'wgbedcgyfqonbntz'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = 'test@yandex.ru'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

USE_I18N = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'style': '{',
#     'formatters': {
#         'debug_form': {
#             'format': '%(asctime)s %(levelname)s %(message)s'
#         },
#         'warning_form': {
#             'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s'
#         },
#         'error_form': {
#             'format': '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'
#         },
#         'general_form': {
#             'format': '%(asctime)s %(levelname)s %(module)s %(message)s'
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         }
#     },
#     'handlers': {
#         'console_debug': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'debug_form'
#         },
#         'console_warning': {
#             'level': 'WARNING',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'warning_form'
#         },
#         'console_error': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'error_form'
#         },
#         'general_log': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'formatter': 'general_form',
#             'filename': 'general.log'
#         },
#         'error_log': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.FileHandler',
#             'formatter': 'error_form',
#             'filename': 'error.log'
#         },
#         'security_log': {
#             'filters': ['require_debug_true'],
#             'class': 'logging.FileHandler',
#             'formatter': 'general_form',
#             'filename': 'security.log'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler',
#             'formatter': 'warning_form'
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console_debug', 'console_warning', 'console_error', 'general_log'],
#             'propagate': True
#         },
#         'django.request': {
#             'handlers': ['error_log', 'mail_admins'],
#             'propagate': True
#         },
#         'django.server': {
#             'handlers': ['error_log', 'mail_admins'],
#             'propagate': True
#         },
#         'django.template': {
#             'handlers': ['error_log'],
#             'propagate': True
#         },
#         'django.db.backends': {
#             'handlers': ['error_log'],
#             'propagate': True
#         },
#         'django.security': {
#             'handlers': ['security_log'],
#             'propagate': True
#         }
#     }
# }
