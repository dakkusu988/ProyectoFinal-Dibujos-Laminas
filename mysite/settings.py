import os
from pathlib import Path
from django.urls import reverse_lazy
import dj_database_url  # Para configurar PostgreSQL
import django_heroku
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary_storage.storage import MediaCloudinaryStorage

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# ---------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# -----------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "clave_por_defecto_no_segura") # SECRET KEY para Render
# SECRET_KEY = '' # SECRET KEY para pruebas en Local

# SECURITY WARNING: don't run with debug turned on in production!
# ------------------------------------------------------------------
DEBUG = os.getenv("DEBUG", "False") == "True" # DEBUG para Render
# DEBUG = True  # DEBUG para pruebas en Local

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.pythonanywhere.com', 'tienda-de-laminas.onrender.com']

# Application definition
# -----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dibujo',
    'api',
    'rest_framework',
    'cloudinary',
    'cloudinary_storage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# --------------------------------------------------------------
# Base de datos para Render (PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        engine='django.db.backends.postgresql'
    )
}

# Base de datos para hacer pruebas en local (SQLite)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# ---------------------------------------------------
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Berlin'

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# -----------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static' # Para usar en Local
# STATIC_ROOT = BASE_DIR / 'staticfiles'  # Para usar en Render

# Configuración para servir archivos estáticos en producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
django_heroku.settings(locals())  # Esto auto configura varias cosas para Render

# PARA LAS IMAGENES
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Configuración de almacenamiento de imágenes
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Se usa para que las imagenes de las Láminas no se borren cuando se reinicia el servidor en Render
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# -----------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Spanish')
]

# PARA EL LOGIN & LOGOUT
LOGIN_REDIRECT_URL = reverse_lazy("detallesUsuario")
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'detallesUsuario'

# Configuración del servidor de correo
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # Pruebas por Consola
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Pruebas por GMAIL
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tiendadelaminas13@gmail.com'
# EMAIL_HOST_PASSWORD = '' # Contraseña de Aplicación en Local
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD") # Contraseña de Aplicación en Render
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
