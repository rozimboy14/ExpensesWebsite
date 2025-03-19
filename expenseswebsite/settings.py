"""
Django settings for expenseswebsite project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Configure Django App for Heroku.
import django_heroku
import dj_database_url
from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ["expenses.uz","www.expenses.uz",'127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "expenses",
    "authentication",
    'userpreferences',
    'userincome',
    'modeltranslation',
    'whitenoise.runserver_nostatic',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "expenseswebsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "expenseswebsite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
import psycopg2

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "incomeexpensesdb",
        "USER": "postgres",
        "PASSWORD": "ojimro011",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
connection = psycopg2.connect(
    dbname=DATABASES["default"]["NAME"],
    user=DATABASES["default"]["USER"],
    password=DATABASES["default"]["PASSWORD"],
    host=DATABASES["default"]["HOST"],
    port=DATABASES["default"]["PORT"],
)

print("PostgreSQL ga muvaffaqiyatli ulandi!")

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "uz-uz"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('uz',_("Uzbek")),
    ('en',_("English")),
    ('ru',_("Russian")),
]
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

LOCALE_PATHS = [BASE_DIR / 'locale']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = ('home/expenses.uz/django/static',)

STATIC_ROOT = 'home/expenses.uz/django/staticfiles'
MEDIA_ROOT='home/expenses.uz/django/media'
django_heroku.settings(locals())

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
from django.contrib import messages
from decouple import config

MESSAGE_TAGS = {
    messages.ERROR: "danger",
}
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_HOST_USER =config("EMAIL_HOST_USER")
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")




# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
