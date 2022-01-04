"""
Django settings for OFX_API project.

Designed & Developed by Narendar Reddy G, OscarFX Studios
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import sys
import ldap
from django_auth_ldap.config import LDAPSearch, LDAPGroupQuery, GroupOfNamesType, LDAPSearchUnion

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTH_LDAP_SERVER_URI = "ldap://192.168.5.2"
AUTH_LDAP_BIND_DN = "pipeline account"

AUTH_LDAP_BIND_PASSWORD = "Gunreddy^999"
AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch("OU=DevelopmentTeam,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=Pipeline,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXMatchmove,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXIT,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXData,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXPaint,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXProdManagement,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXRoto,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXBidding,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXTraining,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
    LDAPSearch("OU=OFXUsers,dc=oscarfx,dc=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)"),
)

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
}

AUTH_LDAP_NO_NEW_USERS = True

AUTHENTICATION_BACKENDS = (
    # "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$qk=xmf1nr6xy)4-!w2g5!wh=)$e6^8@v^z%w@i8n44pjf5lg2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','*']


# Application definition

INSTALLED_APPS = [
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

DRF_API_LOGGER_DATABASE = True

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

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": [('192.168.3.51', '6379')],
#         },
#     },
# }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

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
    import MySQLdb

    connection = MySQLdb.connect(host='192.168.5.21',
                                 port=3306,
                                 user='data_admin',
                                 passwd='Ofx_data_Admin#5262',
                                 )
    cur = connection.cursor()
    cur.execute('CREATE DATABASE IF NOT EXISTS ofx_api;')
    connection.close()
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ofx_api',
            'USER': 'data_admin',
            'PASSWORD': 'Ofx_data_Admin#5262',
            'HOST': '192.168.5.21',
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
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
# if sys.platform == 'linux':
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
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
    },
    'handlers': {
        'core': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOG_PATH + '/ofx_pipeline.log',
            'formatter': 'verbose'
        },
        'console': {
            "class": "logging.StreamHandler",
        }
    },
    'loggers': {
        'django': {
            'handlers': ['core'],
            'level': 'WARNING',
            'propagate': True,
        },
        "django_auth_ldap": {
            "handlers": ["console"],
            "level": "DEBUG",
        }
    },
}

REST_FRAMEWORK = {
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
LOGIN_EXEMPT_URLS = (r'^admin/', r'^api/*', r'^media/', r'^profile/login_custom')

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