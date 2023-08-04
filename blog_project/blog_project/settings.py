from pathlib import Path
from dotenv import load_dotenv
import os
from decouple import config
from .env.injector import SETTINGS_KEYS

BASE_DIR = Path(__file__).resolve().parent.parent

#-------------------------------------------------------------------------------------------------------#
# Secret Values
#-------------------------------------------------------------------------------------------------------#

get_value = SETTINGS_KEYS

django_key = get_value.djky
sql_user_name = get_value.urne
sql_password = get_value.pawd
database_state = get_value.dbstt
email_host = get_value.emht
email_user = get_value.emun
email_password = get_value.empw
email_port = get_value.empt
email_backend = get_value.embe


#-------------------------------------------------------------------------------------------------------#
# Project settings
#-------------------------------------------------------------------------------------------------------#

SECRET_KEY = django_key

DEBUG = database_state

ALLOWED_HOSTS = ['blog.silkthreaddev.com', 'www.blog.silkthreaddev.com']

#-------------------------------------------------------------------------------------------------------#
# SMTP email setup
#-------------------------------------------------------------------------------------------------------#

EMAIL_HOST = email_host
EMAIL_HOST_USER = email_user
EMAIL_HOST_PASSWORD = email_password
EMAIL_PORT = email_port
EMAIL_USE_TLS = True
EMAIL_BACKEND = email_backend

#-------------------------------------------------------------------------------------------------------#
# Base Directory setup
#-------------------------------------------------------------------------------------------------------#

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog_app',
    'members',
    'bootstrap5',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_project.urls'

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

WSGI_APPLICATION = 'blog_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'SILK_THREAD_DEV_BLOG_DB',
        'USER': sql_user_name,
        'PASSWORD': sql_password,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


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
#-------------------------------------------------------------------------------------------------------#
# Time-zone/Language  
#-------------------------------------------------------------------------------------------------------#
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
#-------------------------------------------------------------------------------------------------------#
# Directory and URLS 
#-------------------------------------------------------------------------------------------------------#
STATIC_URL = 'static/'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
