from datetime import timedelta
from pathlib import Path
import os
print("SECRET_KEY:", os.environ.get("SECRET_KEY"))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'Vb8Nw2RqTz6LpYf3Hm4KdXj1Uc7Gs9Ae5Sh0JrQvLZpWxM' 
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment!")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"


ALLOWED_HOSTS = ['localhost','127.0.0.1','railway.com','web-production-8e0fa.up.railway.app','.up.railway.app']

# ////////////////////////////////////////////////////////////
# --- SECURITY / PROXY ---
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# If you're serving over HTTPS (Railway does), secure cookies are a good idea
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# If your frontend is on a different domain and you need cookies cross-site,
# use 'None' (requires Secure). Otherwise 'Lax' is fine.
CSRF_COOKIE_SAMESITE = 'Lax'  # or 'None' if truly cross-site with cookies

# --- CSRF: FULLY-QUALIFIED ORIGINS REQUIRED ---
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-8e0fa.up.railway.app",
    "https://*.up.railway.app",
    # add your custom domain(s) if any:
    # "https://yourdomain.com",
    # "https://www.yourdomain.com",
]

# ////////////////////////////////////////////////////////////

# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'projects.apps.ProjectsConfig',
    'users.apps.UsersConfig',
    'rest_framework',
    'corsheaders',
    'storages', 
]

REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "ON_LOGIN_SUCCESS": "rest_framework_simplejwt.serializers.default_on_login_success",
    "ON_LOGIN_FAILED": "rest_framework_simplejwt.serializers.default_on_login_failed",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'corsheaders.middleware.CorsMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.has_unread_messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD':os.getenv("DB_PASSWORD") ,
        'HOST':os.getenv("DB_HOST") ,
        'PORT': os.getenv("DB_PORT"),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
CORS_ALLOW_ALL_ORIGINS = True


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


EMAIL_BACKEND = EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST =   os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT") 
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == "True"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/images/'


STATICFILES_DIRS=[
   BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / "staticfiles"
# MEDIA_ROOT = BASE_DIR / 'static/images'



# settings.py

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        # "BACKEND": "storages.backends.s3boto3.S3Boto3Storage"

    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Now define AWS options at the top level
AWS_QUERYSTRING_AUTH = os.getenv("AWS_QUERYSTRING_AUTH") == "True"
AWS_S3_FILE_OVERWRITE = os.getenv("AWS_S3_FILE_OVERWRITE") == "True"

AWS_ACCESS_KEY_ID =  os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY =  os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME =  os.getenv("AWS_S3_REGION_NAME")  # e.g., us-east-1
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME") 
# AWS_DEFAULT_ACL = "public-read"
# AWS_DEFAULT_ACL = None  # optional

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = os.getenv("DEFAULT_AUTO_FIELD", "django.db.models.BigAutoField")



LOGGING = {
 'version': 1,
 'disable_existing_loggers': False,
 'handlers': {'console': {'class': 'logging.StreamHandler'}},
 'root': {'handlers': ['console'], 'level': 'ERROR'},
}

if os.getcwd()=='/app':
    DEBUG=False 
