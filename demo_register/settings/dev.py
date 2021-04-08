from demo_register.settings.base import *

DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

# use white noise
STATIC_URL = '/static/'
STATIC_DIR = os.path.join('static')

# DEBUG_TOOLBAR_CONFIG = {
#     'SHOW_TOOLBAR_CALLBACK': lambda r: False,  # disables it
# }


STATICFILES_DIRS = [
    STATIC_DIR,
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'e_learning1',
        'USER': config('POSTGRE_USER'),
        'PASSWORD': config('POSTGRE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'TEST': {
            'NAME': 'testdatabase2',
        },
    }
}

# CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# CELERY_BROKER_URL = ''
#
# CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_BACKEND = 'django-db'

CELERY_CACHE_BACKEND = 'django-cache'


# SITE_ID = 2
#
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }
