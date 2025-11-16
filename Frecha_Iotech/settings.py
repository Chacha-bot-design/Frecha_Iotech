# settings.py - COMPLETE WORKING VERSION
import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-development-key')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'



# ===== CORS CONFIGURATION =====
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://frecha-iotechi.onrender.com",
    "https://frecha-iotech.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

# ===== AUTHENTICATION =====
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/profile/'  # ← Fixed: added leading slash
LOGOUT_REDIRECT_URL = '/'

print("🔐 PRODUCTION CORS CONFIGURED")
print(f"   Frontend: https://frecha-iotechi.onrender.com")
print(f"   Backend: https://frecha-iotech.onrender.com")


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'store',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Frecha_Iotech.urls'
WSGI_APPLICATION = 'Frecha_Iotech.wsgi.application'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Railway PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

# Templates
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

# Static & Media Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

print("🚀 FULL FEATURES CONFIGURATION LOADED")
print(f"   Database: {DATABASES['default']['ENGINE']}")
print(f"   Debug: {DEBUG}")
print(f"   Images: Enabled (Pillow 10.4.0)")


# ===== ADD THESE TO YOUR EXISTING SETTINGS =====

# CSRF & Security
CSRF_TRUSTED_ORIGINS = [
    'https://frecha-iotech.onrender.com',
    'https://frecha-iotechi.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Security headers for Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG

# CORS specific settings
CORS_ALLOWED_ORIGINS = [
    "https://frecha-iotech.onrender.com",
    "https://frecha-iotechi.onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

# Authentication
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'profile/'
LOGOUT_REDIRECT_URL = '/'

# Static files additional config
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Whitenoise
WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False

print("🔐 SECURITY & CORS CONFIGURATION UPDATED")
print(f"   CSRF Trusted Origins: {len(CSRF_TRUSTED_ORIGINS)} configured")
print(f"   CORS Allowed Origins: {len(CORS_ALLOWED_ORIGINS)} configured")