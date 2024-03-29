import os
import environ

import django_heroku

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    STRIPE_LIVE_MODE=(bool, False)
)
environ.Env.read_env()

ALLOWED_HOSTS = ['chaoskasten.com', 'localhost']


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = [
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lazysignup',
    'stripe',
]

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'lazysignup.backends.LazySignupBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'main.wsgi.application'


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_REDIRECT_URL = '/notes'
LOGOUT_REDIRECT_URL = '/'

DOMAIN_URL = env('DOMAIN_URL')

if env.get_value("STRIPE_LIVE_MODE"):
    STRIPE_PUBLIC_KEY = env('STRIPE_LIVE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = env('STRIPE_LIVE_SECRET_KEY')
else:
    STRIPE_PUBLIC_KEY = env("STRIPE_TEST_PUBLIC_KEY")
    STRIPE_SECRET_KEY = env("STRIPE_TEST_SECRET_KEY")


STRIPE_PRICE_ID = env("STRIPE_PRICE_ID")

APPEND_SLASH=False

SECRET_KEY = env('SECRET_KEY')

# false when it does not exist (wtf)
DEBUG = env('DEBUG')

DATABASES = {
    'default': {
    # 'django.db.backends.postgresql_psycopg2' for production
        'ENGINE': env('ENGINE'),
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

SENDGRID_API_KEY = env('SENDGRID_API_KEY')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Activate Django-Heroku.
django_heroku.settings(locals())
