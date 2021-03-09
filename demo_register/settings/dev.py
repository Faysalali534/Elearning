from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

# use white noise
STATIC_URL = '/static/'
STATIC_DIR = os.path.join('static')


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: False,  # disables it
}


STATICFILES_DIRS = [
    STATIC_DIR,
]


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
