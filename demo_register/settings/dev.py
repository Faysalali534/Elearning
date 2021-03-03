from .base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

# use white noise
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

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
