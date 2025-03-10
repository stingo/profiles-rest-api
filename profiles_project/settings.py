"""
Django settings for profiles_project project.

Generated by 'django-admin startproject' using Django 5.1.6.
"""

import os
from pathlib import Path
import dj_database_url  # ✅ Import this!

# ✅ Ensure BASE_DIR is correctly defined
BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ SECRET KEY (Use environment variable in production)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")

# ✅ DEBUG MODE (Set to False in production!)
DEBUG = os.getenv("DEBUG", "True") == "True"

# ✅ Allowed Hosts
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "profiles-rest-api-9mga.onrender.com",  # Add your Render domain here
]

# ✅ Installed Apps
INSTALLED_APPS = [
    'profiles_api',  # Ensure this is above django.contrib.auth
    'corsheaders',  # Allow cross-origin requests

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_countries",  # ✅ Add this

    'rest_framework',
    'rest_framework.authtoken',
    'django_extensions',
]

# ✅ Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 👈 Add this at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True  # 👈 Allow credentials (if needed)

# ✅ Root URL configuration
ROOT_URLCONF = 'profiles_project.urls'

# ✅ Templates
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

# ✅ WSGI Application
WSGI_APPLICATION = 'profiles_project.wsgi.application'

# ✅ Database Settings (Fix!)
if os.getenv("DATABASE_URL"):  # Use database URL if provided
    DATABASES = {
        "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
    }
else:  # Use SQLite as fallback
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ✅ Password Validators
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

# ✅ Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ Static Files
STATIC_URL = "static/"

# ✅ Default Primary Key Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ✅ Custom User Model
AUTH_USER_MODEL = "profiles_api.UserProfile"