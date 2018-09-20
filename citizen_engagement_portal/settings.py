"""
Django settings for citizen_engagement_portal project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from citizen_engagement_portal.password import getpass, getdatabases

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-7%yc)idb7m56wxee1@v4qh-q6aw-jutwq%%8@3%r@+o_)q#v!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', '159.89.111.14', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'social.apps.django_app.default',

    'notifications',
    'social_django',
    'volunteer',
    'social-core-master',
    'disqus',
    'background_task',

]

DISQUS_API_KEY = 'HXEpZnRKJ0xtNiJUnY8Oau3jkERExk41z07gEDFmmtSHXdNZvEwYq7dpAn9s4mRd'
DISQUS_WEBSITE_SHORTNAME = 'Changer'

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'volunteer.get_username.RequestMiddleware',



    # 'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'citizen_engagement_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

                'django.template.context_processors.media',
                 ],

        },
    },
]

WSGI_APPLICATION = 'citizen_engagement_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = getdatabases()

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

USE_I18N = True
LANGUAGE_CODE = 'uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = 'media'

MEDIA_URL = '/media/'


# AUTHENTICATION_BACKENDS = (
#     'social_core.backends.facebook.FacebookOAuth2',
#     'social_core.backends.instagram.InstagramOAuth2',
#     'social.backends.google.GoogleOpenId',
#     'social.backends.google.GoogleOAuth2',
#     'social.backends.google.GoogleOAuth',
#
#     'django.contrib.auth.backends.ModelBackend',
# )


AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',

    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication

    # 'social_core.backends.telegram.TelegramAuth',

    'django.contrib.auth.backends.ModelBackend',
)



TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',

)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

EL_PAGINATION_PER_PAGE = 3

# # Add the google credentials

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '613230157576-6j46bo3jb1i2arb3fll50imcn102r04a.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ER-U8rN8TorZUOCRydbvSeaJ'


SOCIAL_AUTH_FACEBOOK_KEY = '2125271371046613'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'b3bf33810e413c2be7c53e78395c9431'  # App Secret

# SOCIAL_AUTH_TELEGRAM_BOT_TOKEN='672778965:AAExRuzTuJFJHBlhb9oX09rAO-4OYvNkIQ8'
# SECRET_KEY='MyVerySecretKey'



SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'success_oauth'
LOGOUT_REDIRECT_URL = 'login'

# SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['first_name',]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',

    'volunteer.custom_social_pipeline.save_user_name',

    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
#

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'node_modules'),
)

DJANGO_NOTIFICATIONS_CONFIG = { 'USE_JSONFIELD': True}
