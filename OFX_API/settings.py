"""
Django settings for OFX_API project.

Designed & Developed by Narendar Reddy G, OscarFX Studios
"""

#  Copyright (c) 2023.
#  Designed & Developed by Narendar Reddy G, OscarFX Private Limited
#  All rights reserved.

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
from decouple import config

import pymysql

from django.apps import AppConfig

from production.pagination import OFXPagination
from OFX_API.DEFAULTS import DEFAULT_HEADERS

pymysql.install_as_MySQLdb()
# import ldap
# from django_auth_ldap.config import LDAPSearch, LDAPGroupQuery, GroupOfNamesType, LDAPSearchUnion

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# AUTH_LDAP_SERVER_URI = "ldap://192.168.5.2"
# AUTH_LDAP_BIND_DN = "pipeline account"
#
# AUTH_LDAP_BIND_PASSWORD = "Gunreddy^999"
# AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
#     LDAPSearch("OU=DevelopmentTeam,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=Pipeline,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXMatchmove,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXIT,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXData,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXPaint,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXProdManagement,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXRoto,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXBidding,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXTraining,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
#     LDAPSearch("OU=OFXUsers,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
# )
#
# # Populate the Django user from the LDAP directory.
# AUTH_LDAP_USER_ATTR_MAP = {
#     "first_name": "givenName",
#     "last_name": "sn",
# }
#
# AUTH_LDAP_NO_NEW_USERS = False

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTHENTICATION_BACKENDS = (
    # "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$qk=xmf1nr6xy)4-!w2g5!wh=)$e6^8@v^z%w@i8n44pjf5lg2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['127.0.0.1', '*']

# X-XSS-Protection
# SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=False, cast=bool)

## X-Frame-Options
# X_FRAME_OPTIONS = config('XFRAMEOPTIONS', cast=bool)
# #X-Content-Type-Options
# SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', cast=bool)
# # ## Strict-Transport-Security
# if config('STS', cast=bool):
#     SECURE_HSTS_SECONDS = 15768000
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#
# ## that requests over HTTP are redirected to HTTPS. also can config in webserver
# # SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False)
#
# # for more security
# CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast=bool)
# CSRF_USE_SESSIONS = config('CSRF_USE_SESSIONS', cast=bool)
# CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', cast=bool)
# SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', cast=bool)
# SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE', cast=str)

# Application definition

INSTALLED_APPS = [
    'channels',
    'profiles',
    'hrm',
    'production',
    'ofx_dashboards',
    'ofx_statistics',
    'shotassignments',
    'essl',
    'ofx_common',
    'imagekit',
    'rest_framework',
    'rest_framework.authtoken',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_api_logger',
    'corsheaders',
    'colorfield',
    'wsnotifications',
    'history',
    'pipeline_api',
    # 'review',
    'coreapi',  # Coreapi for coreapi documentation
    'drf_yasg',  # drf_yasg fro Swagger documentation
    "log_viewer",
    'time_management',
    'storages',
    'health_check',
    'health_check.db',  # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.s3boto3_storage',  # requires boto3 and S3BotoStorage backend
]

{
    "BACKEND": "django_jinja.backend.Jinja2",
    "OPTIONS": {
        'extensions': ['webpush.jinja2.WebPushExtension'],
    }
},

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'OFX_API.middleware.LoginRequiredMiddleware',
    'OFX_API.middleware.HealthCheckMiddleware',
    'django.middleware.common.CommonMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
    'track_actions.requestMiddleware.RequestMiddleware',
]

CORS_ALLOW_HEADERS = DEFAULT_HEADERS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ['http://10.10.10.10:8000']

ROOT_URLCONF = 'OFX_API.urls'

DRF_API_LOGGER_DATABASE = False

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
                'OFX_API.global_context.password_change'
            ],
        },
    },
]

WSGI_APPLICATION = 'OFX_API.wsgi.application'

# ASGI_APPLICATION = "OFX_API.routing.application"
ASGI_APPLICATION = "OFX_API.asgi.application"

if DEBUG:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [('redis', 6379)],
            },
        },
    }

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', cast=str),
        'USER': config('DB_USERNAME', cast=str),
        'PASSWORD': config('DB_PASSWORD', cast=str),
        'HOST': config('DB_HOST', cast=str),
        'PORT': config('DB_PORT', cast=int)
    },
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = config('SESSION_EXPIRE_AT_BROWSER_CLOSE', default=False, cast=bool)
SESSION_COOKIE_AGE = 43200 #in seconds 12 hours. "1209600(2 weeks)" by default

SESSION_SAVE_EVERY_REQUEST = True # "False" by default

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# STATIC_URL = '/static/'
# USE_S3 = False
#
if config('USE_S3', cast=bool):
    ### AWS STORAGE ####
    AWS_ACCESS_KEY_ID = 'AKIA5EDY7UCE5G4LUOGI'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'ofxsbbucket'
    AWS_S3_CUSTOM_DOMAIN = 'ofxsbbucket.s3.ap-south-1.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = 'static'
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'OFX_API.storage_backends.MediaStorage'  # the media storage configurations
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

import mimetypes

mimetypes.add_type("text/javascript", ".js", True)

if sys.platform == 'linux':
    LOG_PATH = '/tmp/'
else:
    LOG_PATH = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        "handlers": {
            "file": {
                "level": "ERROR",
                "class": "logging.FileHandler",
                "filename": LOG_PATH + "/shotbuzz_debug.log",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["file"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        }
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        }
    }

REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'OFXPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

LOGIN_REDIRECT_URL = r'^home'
LOGIN_URL = '/login/'
LOGIN_EXEMPT_URLS = (
    r'^admin/', r'^api/*', r'^media/', r'^profile/login_custom', r'^accounts/', r'^docs/', r'^health_check/',
    r'^api/user/password_change/')

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    }

"""
Memcached is an entirely memory-based cache server,
The fastest, most efficient type of cache supported natively by Django,
"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcached:11211',  # Use the service name defined in docker-compose.yml
        'TIMEOUT': None,
        'OPTIONS': {
            'server_max_value_length': 1024 * 1024 * 2,
        }
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

LOG_VIEWER_FILES = ['logfile1', 'logfile2', ...]
LOG_VIEWER_FILES_PATTERN = '*.log*'
LOG_VIEWER_FILES_DIR = 'logs/'
LOG_VIEWER_PAGE_LENGTH = 25  # total log lines per-page
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25  # Max log files loaded in Datatable per page
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']

# Optionally you can set the next variables in order to customize the admin:
LOG_VIEWER_FILE_LIST_TITLE = "OFX API LOGS"
LOG_VIEWER_FILE_LIST_STYLES = "/static/css/my-custom.css"

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = {'application/json'}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Europe/Paris'
CELERY_RESULT_BACKEND = 'redis://redis:6379'

EMAIL_USE_TLS = True
# EMAIL_HOST = '124.123.22.16'
EMAIL_HOST = config('EMAIL_HOST')

EMAIL_PORT = 587
EMAIL_HOST_USER = 'shotbuzzalerts@pixrock.org'
EMAIL_HOST_PASSWORD = 'Mail@123'

DEFAULT_FROM_EMAIL = "shotbuzzalerts@pixrock.org"
EMAIL_TIMEOUT = 600
