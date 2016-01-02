"""
Django settings for youtubeadl project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',
                       '^b46d^zsxhrthkq2p7ty14^zov%4@eq@j5e%f(ki_#2rnbp%-l')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # Grappelli needs to be defined before the admin.
    'grappelli',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd-party apps.
    'compressor',
    'django_extensions',

    # Project apps.
    'youtubeadl.apps.core',
    'youtubeadl.apps.downloader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'youtubeadl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Local context processors.
                'youtubeadl.apps.core.context_processors.third_party_tracking_ids',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = 'youtubeadl.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME', 'youtubeadl'),
        'USER': os.getenv('DATABASE_USER', 'youtubeadl'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'password'),
        'HOST': os.getenv('DATABASE_HOST', '127.0.0.1'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.getenv('STATIC_ROOT',
                        os.path.join(BASE_DIR, 'collected_static'))

STATIC_URL = '/static/'

# Additional locations of static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)


# Media files.

MEDIA_ROOT = os.getenv('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

MEDIA_URL = '/media/'


# Email settings.

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'Info <info@youtubeadl.com>'
SERVER_EMAIL = 'Alerts <alerts@youtubeadl.com>'

ADMINS = (
    ('Admin', 'admin@youtubeadl.com'),
)


# Logging settings.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s  [%(name)s:%(lineno)s]  %(levelname)s - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        # Silence SuspiciousOperation.DisallowedHost exception ('Invalid
        # HTTP_HOST' header messages). Set the handler to 'null' so we don't
        # get those annoying emails.
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'handlers': ['console', ],
            'level': 'INFO',
        }
    }
}


# YouTube Audio Downloader settings.
MAX_DURATION_SECONDS = 10800
DAILY_CONVERT_LIMIT = 25


# 3rd-party apps tracking IDs.
GOOGLE_ANALYTICS_TRACKING_ID = os.getenv('GOOGLE_ANALYTICS_TRACKING_ID')
ADDTHIS_PUBLISHER_ID = os.getenv('ADDTHIS_PUBLISHER_ID')


# Celery settings.
BROKER_URL = os.getenv('BROKER_URL', 'amqp://guest:guest@127.0.0.1//')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'amqp')


# Grappelli settings.
GRAPPELLI_ADMIN_TITLE = 'YouTube ADL Admin'