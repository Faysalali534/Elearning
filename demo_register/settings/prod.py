from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

# use white noise

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'e_learning',
        'USER':  os.environ['POSTGRE_USER'],
        'PASSWORD': os.environ['POSTGRE_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
