from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent.parent
env = Env()
env.read_env()

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG")
BASE_URL = env("BASE_URL")

ENVIROMENT_CORE_TOKEN = env("CORE_TOKEN")
TELEGRAM_BOT_WEBHOOK_URL = (
    env.str("TELEGRAM_BOT_WEBHOOK_URL") + ENVIROMENT_CORE_TOKEN + "/"
)
TELEGRAM_BOT_USERNAME = 'TestAssistant1Robot'
# TELEGRAM_BOT_USERNAME = env.str("TELEGRAM_BOT_USERNAME")
DADATA_TOKEN = env("DADATA_TOKEN")
LANDING_ENABLED = env.bool("LANDING_ENABLED")

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} [{asctime}] {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_warning": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/logs/warnings.log",
            "formatter": "verbose",
        },
        "celery_all": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/logs/celery.log",
            "formatter": "verbose",
        },
        "file_all": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"{BASE_DIR}/logs/all.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file_all"],
            "level": "INFO",
            "propagate": True,
        },
        "celery": {
            "handlers": ["file_all"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "timezone_field",
    "phonenumber_field",
    "bootstrap4",
    "django_filters",
    "django_tables2",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_celery_beat",
    "cabinet.apps.CabinetConfig",
    "dispatcher.apps.DispatcherConfig",
    "referral.apps.ReferralConfig",
    "api.apps.ApiConfig",
    "landing.apps.LandingConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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


def get_auth_classes_for_rest_framework():
    if DEBUG:
        return [
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.TokenAuthentication",
        ]
    else:
        return ["rest_framework.authentication.TokenAuthentication"]


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': get_auth_classes_for_rest_framework(),
#     # "DATETIME_FORMAT": "%m-%d-%Y %H:%M:%S"
# }


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.EnvironmentTokenAuthentication",
    ],
    # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}

WSGI_APPLICATION = "core.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}


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

AUTH_USER_MODEL = "cabinet.User"
LOGIN_REDIRECT_URL = "cabinet:index"
LOGIN_URL = "cabinet:login"

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

#
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_URL = "/static/"
if DEBUG:
    STATIC_ROOT = BASE_DIR.joinpath("static")
else:
    # STATICFILES_DIRS = [BASE_DIR / 'static']
    STATIC_ROOT = BASE_DIR.joinpath("static")
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.joinpath("media")


CELERY_TIMEZONE = "Europe/Moscow"
CELERY_BROKER_TRANSPORT_OPTIONS = {"fanout_prefix": True, "fanout_patterns": True}
