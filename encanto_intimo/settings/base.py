"""
Configurações base do Django para o projeto Encanto Íntimo.

Este arquivo contém todas as configurações comuns que são compartilhadas
entre os ambientes de desenvolvimento e produção.
"""

from pathlib import Path
import os
from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Nota: Ajustamos o BASE_DIR porque agora estamos em um subdiretório
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default="django-insecure-m5pj#31ohb2(qo%kd&qa&t77_qc+21b0tp%1ey!gut@_!!+6df")


# Application definition
INSTALLED_APPS = [
    # Django Core Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # Necessário para allauth
    
    # Third Party Apps - Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    
    # Third Party Apps - Outros
    'crispy_forms',
    'crispy_tailwind',
    'widget_tweaks',
    
    # Local Apps
    'produtos',
    'pedidos',
    'usuarios',
    'fornecedores',
    'carrinho',
    'pagamentos',
    'adminpanel',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # Necessário para allauth
]

ROOT_URLCONF = "encanto_intimo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "carrinho.context_processors.carrinho",
                # Allauth context processors
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "encanto_intimo.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"


# Authentication URLs
LOGIN_URL = '/usuarios/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# Messages Framework
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}


# Session Configuration
SESSION_COOKIE_AGE = 1209600  # 2 semanas
CART_SESSION_ID = 'cart'


# Email Configuration (Base - será sobrescrito nos ambientes específicos)
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@encantointimo.com')


# Payment Gateways Configuration
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
MERCADOPAGO_ACCESS_TOKEN = config('MERCADOPAGO_ACCESS_TOKEN', default='')
MERCADOPAGO_PUBLIC_KEY = config('MERCADOPAGO_PUBLIC_KEY', default='')


# Logging Configuration (Base)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'encanto_intimo': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ===========================
# DJANGO-ALLAUTH CONFIGURATION
# ===========================

# Site framework (necessário para allauth)
SITE_ID = 1

# Backends de autenticação
AUTHENTICATION_BACKENDS = [
    # Backend padrão do Django (para login com username/password)
    'django.contrib.auth.backends.ModelBackend',
    
    # Backend do allauth (para login social)
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configurações do django-allauth (versão atualizada)
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # 'mandatory', 'optional' ou 'none'
ACCOUNT_UNIQUE_EMAIL = True

# Nova sintaxe para campos de signup e métodos de login
ACCOUNT_SIGNUP_FIELDS = ['email']  # Apenas email é obrigatório
ACCOUNT_LOGIN_METHODS = {'email'}  # Login apenas com email

# Nova sintaxe para rate limiting
ACCOUNT_RATE_LIMITS = {
    'login_failed': '5/5m',  # 5 tentativas por 5 minutos
}

# URLs de redirecionamento
LOGIN_REDIRECT_URL = '/usuarios/perfil/'  # Redireciona para o perfil após login
LOGOUT_REDIRECT_URL = '/'  # Redireciona para home após logout
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# Configurações do provedor Google
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID', default=''),
            'secret': config('GOOGLE_CLIENT_SECRET', default=''),
            'key': ''
        }
    }
}

# Configurações adicionais
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'

# Adaptadores personalizados
ACCOUNT_ADAPTER = 'usuarios.adapters.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'usuarios.adapters.CustomSocialAccountAdapter'
