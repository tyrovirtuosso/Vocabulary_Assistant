from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-5#k*5ghkw8wzyw_x9p#4z4h5=-+n_z(c9jea677vdh15154@v@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Needed for "django.contrib.sites" property of Auth
SITE_ID = 1


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Authentication Related Apps
    "django.contrib.sites",
    "allauth", 
    "allauth.account",
    "allauth.socialaccount", 
    
    # ... include the providers you want to enable:
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.apple",
    # "allauth.socialaccount.providers.facebook", 
    # "allauth.socialaccount.providers.instagram",
    # "allauth.socialaccount.providers.telegram",
    # "allauth.socialaccount.providers.twitter",
    
    
    # My Apps
    "learningapp",
    "authenticationApp",
    
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'account_login'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    # Add the allauth middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "Tyro2Virtuoso.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ BASE_DIR / "templates" ], # custom
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

WSGI_APPLICATION = "Tyro2Virtuoso.wsgi.application"

'''
# Default Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
'''
# Connecting to Custom Serverless Cloud PostgreSQL DB
HOST=os.environ.get('AWS_POSTGRE_HOST')
USER=os.environ.get('AWS_POSTGRE_USERNAME')
PASSWORD=os.environ.get('AWS_POSTGRE_PASSWORD')
PORT=int(os.environ.get('AWS_POSTGRE_PORT'))
DATABASE=os.environ.get('AWS_POSTGRE_DATABASE')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': PORT,
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

'''
For Github
https://github.com/settings/applications/new
http://127.0.0.1:8000/accounts/github/login/callback

'''

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'github': {
        'APP': {
            'client_id': os.environ.get('GITHUB_OAUTH_CLIENT_ID'),
            'secret': os.environ.get('GITHUB_OAUTH_CLIENT_SECRET'),
            'key': ''
        }
    },
    
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_OAUTH_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
    
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# The below "BASE_DIR / "static" " uses python3.4's pathlib for defining filesystem paths
STATICFILES_DIRS = [
    BASE_DIR / "static"
]

# File path for production
# When I do "python manage.py collectstatic", all the static files from development will be copied to the static path for production
STATIC_ROOT = BASE_DIR.parent / "local-cdn" / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# Email File Based Test
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'emails'