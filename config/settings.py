import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Завантаження змінних середовища
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Безпека
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-u7y@ti=ccoq#u0%fg)wb(v-j$_36tn(_t)mmr)=cl-1apx5i!^')
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'web']
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8080', 'http://localhost:8080']

# 3. Список застосунків
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'recipes',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 4. База даних (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE', 'recipe_db'),
        'USER': os.environ.get('PGUSER', 'recipe_user'),
        'PASSWORD': os.environ.get('PGPASSWORD', 'recipe_password'),
        'HOST': os.environ.get('PGHOST', 'db'),
        'PORT': os.environ.get('PGPORT', '5432'),
    }
}

# Налаштування мови та часу
LANGUAGE_CODE = 'uk-ua'
TIME_ZONE = 'Europe/Kyiv'
USE_I18N = True
USE_TZ = True

# 5. Статика та Медіа
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Авторизація
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 6. Celery та Redis
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'