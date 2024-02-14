import os
from pathlib import Path
from dotenv import load_dotenv

# Determine the base directory of the project. This is used to construct absolute paths.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a .env file located in the project's root directory.
load_dotenv()

# SECURITY SETTINGS:
# SECRET_KEY is crucial for security, should be kept secret in production, and loaded from an environment variable.
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# DEBUG mode controls whether detailed error pages are shown. Should be False in production for security reasons.
DEBUG = True

# A list of strings representing the host/domain names that this Django site can serve.
ALLOWED_HOSTS = []

# APPLICATION DEFINITION:
# INSTALLED_APPS contains all Django applications that are activated for this Django project.
INSTALLED_APPS = [
    'django.contrib.admin',  # Enables the admin interface.
    'django.contrib.auth',  # Authentication system.
    'django.contrib.contenttypes',  # Framework for content types.
    'django.contrib.sessions',  # Session framework.
    'django.contrib.messages',  # Messaging framework.
    'django.contrib.staticfiles',  # Framework for managing static files.
    'shop',  # Custom app for the shop functionality.
    'social_django',  # Django extension for social authentication.
]

# MIDDLEWARE is a list of middleware to use during request/response processing.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF points to the URL configurations of the Django project.
ROOT_URLCONF = 'eshop.urls'

# TEMPLATES configuration specifies how Django loads and renders templates.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # List of directories to search for template files.
        'APP_DIRS': True,  # Whether to search for templates in each application's "templates" directory.
        'OPTIONS': {
            'context_processors': [
                # Context processors add variables to the context of a template.
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.categories_context',  # Custom context processor for the shop app.
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# WSGI_APPLICATION points to the WSGI callable that Django uses to communicate with the server.
WSGI_APPLICATION = 'eshop.wsgi.application'

# DATABASES configuration defines the settings for the project's database(s).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine (SQLite in this case).
        'NAME': BASE_DIR / 'db.sqlite3',  # Database name.
    }
}

# AUTH_PASSWORD_VALIDATORS is a list of validators that are used to check the strength of user passwords.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# AUTHENTICATION_BACKENDS list authentication schemes for the project.
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',  # Default authentication backend.
)

# Internationalization and localization settings:
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True  # Enable Django's internationalization system.
USE_TZ = True    # Enable timezone support.

# Static files (CSS, JavaScript, Images) configuration:
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration:
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Login and logout redirect URLs:
LOGIN_REDIRECT_URL = 'home'  # URL to redirect to after a successful login.
LOGOUT_REDIRECT_URL = '/'    # URL to redirect to after logging out.

# Social authentication configuration for GitHub and Google:
SOCIAL_AUTH_GITHUB_KEY = str(os.getenv('GITHUB_KEY'))
SOCIAL_AUTH_GITHUB_SECRET = str(os.getenv('GITHUB_SECRET'))
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = str(os.getenv('GOOGLE_KEY'))
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = str(os.getenv('GOOGLE_SECRET'))

# Email configuration:
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'rikimati@rikimati.com'
EMAIL_HOST_PASSWORD = 'RatM233099.-/'

# Session cookie age (in seconds):
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days.

# Default primary key field type for models:
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

