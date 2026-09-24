"""
Django settings for romatravel project.
"""

from pathlib import Path


# ==================================================
# RUTA PRINCIPAL DEL PROYECTO
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# CONFIGURACIÓN GENERAL
# ==================================================

SECRET_KEY = 'django-insecure-romatravel-proyecto'

DEBUG = True

ALLOWED_HOSTS = []


# ==================================================
# APLICACIONES INSTALADAS
# ==================================================

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicación Roma Travel
    'agencia',
]


# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==================================================
# URL PRINCIPAL
# ==================================================

ROOT_URLCONF = 'romatravel.urls'


# ==================================================
# TEMPLATES
# ==================================================

TEMPLATES = [

    {

        'BACKEND':
            'django.template.backends.django.DjangoTemplates',

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


# ==================================================
# WSGI
# ==================================================

WSGI_APPLICATION = 'romatravel.wsgi.application'


# ==================================================
# BASE DE DATOS
# MariaDB / MySQL - XAMPP
# ==================================================

DATABASES = {

    'default': {

        'ENGINE':
            'django.db.backends.mysql',

        'NAME':
            'roma_travel',

        'USER':
            'root',

        'PASSWORD':
            '',

        'HOST':
            '127.0.0.1',

        'PORT':
            '3307',

    }

}


# ==================================================
# VALIDADORES DE CONTRASEÑA
# ==================================================

AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME':
            'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.MinimumLengthValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.CommonPasswordValidator',
    },

    {
        'NAME':
            'django.contrib.auth.password_validation.NumericPasswordValidator',
    },

]


# ==================================================
# IDIOMA Y ZONA HORARIA
# ==================================================

LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# ==================================================
# ARCHIVOS ESTÁTICOS
# CSS - IMÁGENES - JAVASCRIPT
# ==================================================

STATIC_URL = 'static/'


# ==================================================
# CLAVE PRIMARIA AUTOMÁTICA
# ==================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
