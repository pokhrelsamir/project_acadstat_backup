import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-secret-key'
DEBUG = True
ALLOWED_HOSTS = [
    'djangoacadstat.vercel.app',
    'localhost',
    '127.0.0.1',

]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
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

ROOT_URLCONF = 'academicsys.urls'

TEMPLATES = [{
'BACKEND': 'django.template.backends.django.DjangoTemplates',
'DIRS': [BASE_DIR / 'templates'],
'APP_DIRS': True,
'OPTIONS': {'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
'django.template.context_processors.csrf',  # Required for {% csrf_token %}
]},
}]

WSGI_APPLICATION = 'academicsys.wsgi.application'

# Database configuration - using existing PostgreSQL database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'acadstatmain',
        'USER': 'samir',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    ]

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Admin custom settings
ADMIN_SITE_HEADER = 'Academic System'
ADMIN_SITE_TITLE = 'Academic Admin'
ADMIN_INDEX_TITLE = 'Dashboard'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # preserved

# ── Email & SMS Settings (A1) ─────────────────────────────────────────────────
# Configure via environment variables:
#   EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
#   EMAIL_USE_TLS, DEFAULT_FROM_EMAIL
# Console backend (default) logs to stdout instead of sending real mail.
import os as _os

EMAIL_BACKEND = _os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend'  # safe default for dev
)
EMAIL_HOST = _os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(_os.environ.get('EMAIL_PORT', '587'))
EMAIL_HOST_USER = _os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = _os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = _os.environ.get('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
DEFAULT_FROM_EMAIL = _os.environ.get('DEFAULT_FROM_EMAIL', 'AcadStat <noreply@acadstat.com>')

# ── RBAC Middleware (A6) ──────────────────────────────────────────────────────
MIDDLEWARE += ['core.middleware.RolePermissionMiddleware']
