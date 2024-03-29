import os
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True),
    DEBUG_TOOLBAR=(bool, True),
)

# reading .env.docker file
environ.Env.read_env(os.path.join(BASE_DIR, ".env.docker"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-meh6xffm+*auo8m(*g(&jppukv7j4eq$d19+mw$63@hp2ygy(2",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = tuple(env.list("ALLOWED_HOSTS", default=["*"]))

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "rest_framework",
    "rest_framework.authtoken",
    "django_extensions",
    "modeltranslation",
    "django_countries",
    "drf_spectacular",
    # Local
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Debug Toolbar
DEBUG_TOOLBAR = env("DEBUG_TOOLBAR")

if DEBUG and DEBUG_TOOLBAR:
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
    ]
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    INSTALLED_APPS += [
        "debug_toolbar",
    ]

ROOT_URLCONF = "weather.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "weather.wsgi.application"

# Database
# https://docs.we.com/en/5.0/ref/settings/#databases

SQLITE_PATH = BASE_DIR / "db.sqlite3"
DATABASES = {
    "default": env.db(
        default=f"sqlite:///{SQLITE_PATH}"
    ),  # 'default': env.db('SQLITE_URL')
}

# Password validation
# https://docs.weather.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.weather.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ("en", gettext("English")),
    ("ar", gettext("Arabic")),
    ("de", gettext("German")),
)

# Static files (CSS, JavaScript, Images)
# https://docs.weather.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.weather.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "log.log"),
            "formatter": "verbose",
            "maxBytes": 1024 * 1024 * 100,  # 100MB
            "backupCount": 10,
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "propagate": True,
            "level": "INFO",
        },
        "": {
            "handlers": ["file", "console"],
            "level": "INFO",
        },
    },
}
CACHE_SECONDS = env("CACHE_SECONDS", default=300)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        'LOCATION': env.cache_url()['LOCATION'],
        "TIMEOUT": CACHE_SECONDS,
    }
}


AUTH_USER_MODEL = "core.User"

OPEN_WEATHER_API_KEY = env(
    "OPEN_WEATHER_API_KEY", default="40e81b0386bf3086563e5fe4ec67e22b"
)
BASE_API_URL = env("BASE_API_URL", default="http://api.openweathermap.org/")
