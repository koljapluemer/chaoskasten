from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm@h7p579ti3&eu5pxya87&pck@t_52djb6_!4y7^pg*c97nax+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['142.93.110.128', 'localhost', '7293aead.ngrok.io', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
