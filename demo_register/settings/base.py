import os
from datetime import timedelta

from decouple import config
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '62mne3w7&!4kx$uhc-b09rsdvlj#elkng^6klvy*=hza7j=1rr'
# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'debug_toolbar',
    'rest_framework',
    'crontab',
    'django_celery_results',
    'django_celery_beat',
    # 'rest_framework.authtoken',

    'accounts.apps.AccountsConfig',
    'learning_material.apps.LearningMaterialConfig',
    'restapi.apps.RestapiConfig',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    'rest_framework_swagger',
    'djoser',
    'social_django',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}
# REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }
# AUTH_USER_MODEL = 'accounts.UserInfo'

MIDDLEWARE = [
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'demo_register.middleware.LoginRequiredMiddleware',
    # 'demo_register.middleware.ExceptionMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'demo_register.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'demo_register.wsgi.application'


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


LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/accounts/login/'

LOGIN_EXEMPT_URLS = (
    r'^accounts/logout/$',
    r'^accounts/register/$',
    r'^restapi/profile_create/$',
    r'^restapi/profile_get/$',
    r'^restapi/update_user/$',
    r'^restapi/delete_user/$',
    r'^restapi/user_profile_api/$',
    r'^restapi/UserAPI/$',
    r'^gettoken/$',
    r'^verify_token/$',
    r'^refresh_token/$',
    r'^learning_material_api/course_info_api/$',
    # r'^social_account/login/$',
    r'^restapi/google/$',
)

INTERNAL_IPS = [
    '127.0.0.1',
]

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'AUTH_TOKEN_CLASSES': (
    #     'rest_framework_simplejwt.tokens.AccessToken'
    # )
}

DJOSER = {
    # 'LOGIN_FIELD': 'username',
    # 'USER_CREATE_PASSWORD_RETYPE': True,
    # 'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,
    # 'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    # 'SEND_CONFIRMATION_EMAIL': False,
    # 'SET_USERNAME_RETYPE': True,
    # 'SET_PASSWORD_RETYPE': True,
    # 'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL': 'activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': False,
    'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
    # 'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': ['http://127.0.0.1:8002'],
    'SERIALIZERS': {
        'user_create': 'restapi.serializers.UserCreateSerializer',
        'user': 'restapi.serializers.UserCreateSerializer',
        'current_user': 'restapi.serializers.UserCreateSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
}

SOCIAL_AUTH_GOOGLE_KEY = '993340120000-keb638moekcpkivo0v1h8qhqq3rpifs4.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_SECRET = 'Q5RQ38sZE7Zr0qWWHnXNwf41'
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo/profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    'firstname',
    'lastname'
]