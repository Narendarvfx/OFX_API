"""
Django settings for OFX_API project.

Designed & Developed by Narendar Reddy G, OscarFX Studios
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
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

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

AUTHENTICATION_BACKENDS = (
    # "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$qk=xmf1nr6xy)4-!w2g5!wh=)$e6^8@v^z%w@i8n44pjf5lg2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','*']

# # X-XSS-Protection
# SECURE_BROWSER_XSS_FILTER = True
#
# ## X-Frame-Options
# X_FRAME_OPTIONS = 'DENY'
# #X-Content-Type-Options
# SECURE_CONTENT_TYPE_NOSNIFF = True
# ## Strict-Transport-Security
# SECURE_HSTS_SECONDS = 15768000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
#
# ## that requests over HTTP are redirected to HTTPS. also can config in webserver
# SECURE_SSL_REDIRECT = True
#
# # for more security
# CSRF_COOKIE_SECURE = True
# CSRF_USE_SESSIONS = True
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = True
# SESSION_COOKIE_SAMESITE = 'Strict'

# Application definition

INSTALLED_APPS = [
    'common',
    'profiles',
    'hrm',
    'production',
    'essl',
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
    'channels',
    'notifications',
    'coreapi', # Coreapi for coreapi documentation
    'drf_yasg', # drf_yasg fro Swagger documentation
    "log_viewer"
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
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'OFX_API.middleware.LoginRequiredMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'OFX_API.urls'

DRF_API_LOGGER_DATABASE = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

ASGI_APPLICATION = "OFX_API.routing.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', '6379')],
        },
    },
}

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ofx_api',
            'USER': 'root',
            'PASSWORD': 'VggGa6Kwq4bq',
            'HOST': '127.0.0.1',
            'PORT': '3306'
        },
    }

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

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

if sys.platform == 'linux':
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

if sys.platform == 'linux':
    LOG_PATH = '/tmp/'
else:
    LOG_PATH = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

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
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'PAGINATE_BY': 10,
}

LOGIN_REDIRECT_URL = r'^home'
LOGIN_URL = '/login/'
LOGIN_EXEMPT_URLS = (r'^admin/', r'^api/*', r'^media/', r'^profile/login_custom', r'^accounts/')

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
        'LOCATION': '127.0.0.1:11211',
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
LOG_VIEWER_PAGE_LENGTH = 25       # total log lines per-page
LOG_VIEWER_MAX_READ_LINES = 1000  # total log lines will be read
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25 # Max log files loaded in Datatable per page
LOG_VIEWER_PATTERNS = ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]']

# Optionally you can set the next variables in order to customize the admin:
LOG_VIEWER_FILE_LIST_TITLE = "OFX API LOGS"
LOG_VIEWER_FILE_LIST_STYLES = "/static/css/my-custom.css"
