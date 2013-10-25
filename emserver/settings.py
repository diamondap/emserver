import logging
import sys

"""
Django settings for emserver project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FIXTURE_DIRS = os.path.join(BASE_DIR, 'fixtures')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a$e)-nr+sdnfu1i8*o=-=am_y00o*gb5j=k!8o4qj2i14v6fb@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ADMIN_ENABLED = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'em',
    'rest_framework',
    #'pagination',
    'sorting_bootstrap',
    'django_filters',
    'crispy_forms',
    'django_nose'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'emserver.urls'

WSGI_APPLICATION = 'emserver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'em',
        'USER': 'evilmommy',
        'PASSWORD': 'aX4d71311HNzd.9',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        #'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ]
}



class NoMessageFailuresFilter(logging.Filter):
    """
    Suppress warnings from Django messaging, or you'll get tons of these
    when you run your tests. Apparently the messaging tests are not being
    maintained, or they are just wrong. This code was taken from
    https://github.com/omab/django-social-auth/issues/283
    """
    def filter(self, record):
        if record.exc_info:
            from django.contrib.messages.api import MessageFailure
            exception = record.exc_info[1]
            if isinstance(exception, MessageFailure):
                return False
        return True

# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'no_message_failures': {
            '()': NoMessageFailuresFilter,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'semi-verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stderr,
        },
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'semi-verbose',
            'stream': sys.stderr
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            'filters': ['no_message_failures'],
        },
        'default': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
            'filters': [],
        },
        'dev': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
            'filters': [],
        },
    }
}
