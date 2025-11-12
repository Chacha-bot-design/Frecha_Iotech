"""
Django settings for Frecha_Iotech project.
PRODUCTION-READY for Railway (PostgreSQL) + Render (Backend/Frontend)
"""

from pathlib import Path
import os
import dj_database_url
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============ PRODUCTION SECURITY SETTINGS ============
SECRET_KEY = os.environ.get('SECRET_KEY', get_random_secret_key())
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Render domains - update these with your actual Render domains
BACKEND_DOMAIN = os.environ.get('BACKEND_DOMAIN', 'frecha-iotech.onrender.com')
FRONTEND_DOMAIN = os.environ.get('FRONTEND_DOMAIN', 'frecha-iotechi.onrender.com')

ALLOWED_HOSTS = [
    BACKEND_DOMAIN,
    FRONTEND_DOMAIN,
]

# Development settings
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1', '0.0.0.0'])

# ============ SECURITY HEADERS & MIDDLEWARE ============
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    
    # Local apps
    'store',
]

MIDDLEWARE = [
    # Security and CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    # Django core
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Frecha_Iotech.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'build')
        ],
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

WSGI_APPLICATION = 'Frecha_Iotech.wsgi.application'

# ============ RAILWAY POSTGRESQL CONFIGURATION ============
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Railway PostgreSQL configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    print(f"🔧 Configuring Railway PostgreSQL database...")
    try:
        # Railway provides DATABASE_URL in postgresql:// format
        DATABASES['default'] = dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
        print("✅ Railway PostgreSQL configured successfully")
        print(f"   Database: {DATABASES['default'].get('ENGINE', 'Unknown')}")
        print(f"   Host: {DATABASES['default'].get('HOST', 'Unknown')}")
        print(f"   Name: {DATABASES['default'].get('NAME', 'Unknown')}")
    except Exception as e:
        print(f"❌ Railway Database configuration error: {e}")
        print("🔄 Falling back to SQLite")
else:
    print("ℹ️  No DATABASE_URL found, using SQLite (development)")

# ============ PASSWORD & AUTHENTICATION ============
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 10,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Session security
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG

# CSRF security
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG
CSRF_USE_SESSIONS = False

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============ CORS SECURITY CONFIGURATION ============
CORS_ALLOWED_ORIGINS = [
    f"https://{BACKEND_DOMAIN}",
    f"https://{FRONTEND_DOMAIN}",
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{BACKEND_DOMAIN}",
    f"https://{FRONTEND_DOMAIN}",
]

CORS_ALLOW_CREDENTIALS = True

# Secure CORS methods
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Development CORS settings
if DEBUG:
    CORS_ALLOWED_ORIGINS.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ])
    CSRF_TRUSTED_ORIGINS.extend([
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ])

# ============ REST FRAMEWORK PRODUCTION CONFIG ============
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # TEMPORARY for testing
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

# Development API settings
if DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

# ============ PRODUCTION SECURITY ENFORCEMENT ============
if not DEBUG:
    # HTTPS/SSL Enforcement
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS Settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Security headers
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Proxy settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # File upload security
    FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
    DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
    
    # Static files
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============ PRODUCTION LOGGING ============
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'production.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

print(f"🚀 Configuration Summary:")
print(f"   Backend: {BACKEND_DOMAIN}")
print(f"   Frontend: {FRONTEND_DOMAIN}")
print(f"   Database: {'Railway PostgreSQL' if DATABASE_URL else 'SQLite (Dev)'}")
print(f"   Debug: {DEBUG}")