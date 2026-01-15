# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # Load .env variables
# load_dotenv()

# # -------------------------------------------------
# # BASE CONFIG
# # -------------------------------------------------
# BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

# DEBUG = True

# ALLOWED_HOSTS = ["*"]

# # -------------------------------------------------
# # GEMINI API KEY
# # -------------------------------------------------
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# # -------------------------------------------------
# # APPLICATIONS
# # -------------------------------------------------
# INSTALLED_APPS = [
#     # Django core
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "django.contrib.sites",

#     # Third-party
#     "channels",
#     "rest_framework",

#     # Allauth (OAuth)
#     "allauth",
#     "allauth.account",
#     "allauth.socialaccount",
#     "allauth.socialaccount.providers.google",
#     "allauth.socialaccount.providers.facebook",

#     # Local apps
#     "app",
# ]

# SITE_ID = 1

# # -------------------------------------------------
# # AUTHENTICATION BACKENDS
# # -------------------------------------------------
# AUTHENTICATION_BACKENDS = [
#     "django.contrib.auth.backends.ModelBackend",
#     "allauth.account.auth_backends.AuthenticationBackend",
# ]

# # -------------------------------------------------
# # ALLAUTH SETTINGS (SAFE DEFAULTS)
# # -------------------------------------------------
# ACCOUNT_AUTHENTICATION_METHOD = "username_email"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_USERNAME_REQUIRED = True
# SOCIALACCOUNT_LOGIN_ON_GET = True
# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# ACCOUNT_FORMS = {
#     "signup": "allauth.account.forms.SignupForm",
# }



# LOGIN_URL = "/"
# LOGIN_REDIRECT_URL = "/dashboard/"
# LOGOUT_REDIRECT_URL = "/"

# # -------------------------------------------------
# # MIDDLEWARE
# # -------------------------------------------------
# MIDDLEWARE = [
#     "django.middleware.security.SecurityMiddleware",
#     "django.contrib.sessions.middleware.SessionMiddleware",
#     "django.middleware.common.CommonMiddleware",
#     "django.middleware.csrf.CsrfViewMiddleware",
#     "django.contrib.auth.middleware.AuthenticationMiddleware",
#     "allauth.account.middleware.AccountMiddleware",
#     "django.contrib.messages.middleware.MessageMiddleware",
# ]

# # -------------------------------------------------
# # URL / TEMPLATES
# # -------------------------------------------------
# ROOT_URLCONF = "emotion_assistant.urls"

# TEMPLATES = [
#     {
#         "BACKEND": "django.template.backends.django.DjangoTemplates",
#         "DIRS": [BASE_DIR / "templates"],
#         "APP_DIRS": True,
#         "OPTIONS": {
#             "context_processors": [
#                 "django.template.context_processors.debug",
#                 "django.template.context_processors.request",  # REQUIRED for allauth
#                 "django.contrib.auth.context_processors.auth",
#                 "django.contrib.messages.context_processors.messages",
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = "emotion_assistant.wsgi.application"
# ASGI_APPLICATION = "emotion_assistant.asgi.application"

# # -------------------------------------------------
# # CHANNELS
# # -------------------------------------------------
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",
#     }
# }

# # -------------------------------------------------
# # DATABASE
# # -------------------------------------------------
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# # -------------------------------------------------
# # PASSWORD VALIDATION (disabled for dev)
# # -------------------------------------------------
# AUTH_PASSWORD_VALIDATORS = []

# # -------------------------------------------------
# # INTERNATIONALIZATION
# # -------------------------------------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "Asia/Kolkata"

# USE_I18N = True
# USE_TZ = True

# # -------------------------------------------------
# # STATIC & MEDIA FILES
# # -------------------------------------------------
# STATIC_URL = "/static/"
# STATICFILES_DIRS = [BASE_DIR / "static"]

# MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"

# # -------------------------------------------------
# # DEFAULT FIELD
# # -------------------------------------------------
# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# -------------------------------------------------
# LOAD ENV VARIABLES
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# BASE CONFIG
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

# DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
DEBUG= True

# ALLOWED_HOSTS = [
#     ".onrender.com",
#     "localhost",
#     "127.0.0.1",
# ]
ALLOWED_HOSTS = [
    "remindcare-29.onrender.com",
    "localhost",
    "127.0.0.1",
]



# -------------------------------------------------
# GEMINI API KEY
# -------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -------------------------------------------------
# APPLICATIONS
# -------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Third-party
    "channels",
    "rest_framework",

    # Allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.facebook",

    # Local apps
    "app",

]

SITE_ID = 1

# -------------------------------------------------
# AUTHENTICATION BACKENDS
# -------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# -------------------------------------------------
# ALLAUTH (UPDATED – NO DEPRECATION WARNINGS)
# -------------------------------------------------
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    "username*",
    "password1*",
    "password2*",
]

ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/"

# -------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# -------------------------------------------------
# URL / TEMPLATES
# -------------------------------------------------
ROOT_URLCONF = "emotion_assistant.urls"

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

WSGI_APPLICATION = "emotion_assistant.wsgi.application"
ASGI_APPLICATION = "emotion_assistant.asgi.application"

# -------------------------------------------------
# CHANNELS (DEV SAFE)
# -------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# -------------------------------------------------
# DATABASE
# -------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
    )
}

# -------------------------------------------------
# PASSWORD VALIDATION (DISABLED)
# -------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# -------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True
USE_TZ = True

# -------------------------------------------------
# STATIC & MEDIA FILES
# -------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Create this folder if it doesn’t exist
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------------------------
# SECURITY (FIXED CSRF ERROR)
# -------------------------------------------------
# CSRF_TRUSTED_ORIGINS = [
#     origin for origin in os.environ.get(
#         "CSRF_TRUSTED_ORIGINS", ""
#     ).split(",") if origin
# ]
CSRF_TRUSTED_ORIGINS = [
    "https://remindcare-29.onrender.com",
]


# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"


# -------------------------------------------------
# DEFAULT FIELD
# -------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
