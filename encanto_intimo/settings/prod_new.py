"""
Configurações de Produção - Encanto Íntimo.

Este arquivo contém configurações específicas para o ambiente de produção,
incluindo configurações de segurança, otimizações de performance e
configurações para serviços em nuvem.

IMPORTANTE: Nunca execute em produção com DEBUG=True!
"""

from .base import *
from decouple import config
import os

# SECURITY: DEBUG deve ser FALSE em produção!
DEBUG = config('DEBUG', default=False, cast=bool)

# Hosts permitidos em produção
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

# Database para produção - MySQL configurado para produção
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('PROD_DB_NAME', default='db_encanto'),
        'USER': config('PROD_DB_USER', default='encanto_admin'),
        'PASSWORD': config('PROD_DB_PASSWORD'),
        'HOST': config('PROD_DB_HOST', default='localhost'),
        'PORT': config('PROD_DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'STRICT_TRANS_TABLES',
            'init_command': "SET FOREIGN_KEY_CHECKS = 1;",
            'isolation_level': 'read committed',
            'autocommit': True,
            'ssl_disabled': config('MYSQL_SSL_DISABLED', default=False, cast=bool),
        },
        'CONN_MAX_AGE': 300,  # 5 minutos para produção
        'CONN_HEALTH_CHECKS': True,
    }
}

# Configurações de Segurança para HTTPS em Produção
if not DEBUG:
    # SSL/HTTPS obrigatório
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)  # 1 ano
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
    
    # Cookies seguros
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    SESSION_COOKIE_HTTPONLY = config('SESSION_COOKIE_HTTPONLY', default=True, cast=bool)
    CSRF_COOKIE_HTTPONLY = config('CSRF_COOKIE_HTTPONLY', default=True, cast=bool)
    
    # Proteção adicional
    SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool)
    SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=bool)
    X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default='DENY')
    
    # Proxy reverso (Nginx, etc)
    USE_X_FORWARDED_HOST = config('USE_X_FORWARDED_HOST', default=True, cast=bool)
    USE_X_FORWARDED_PORT = config('USE_X_FORWARDED_PORT', default=True, cast=bool)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cache para produção (opcional - Redis/Memcached)
CACHES = {
    'default': {
        'BACKEND': config(
            'CACHE_BACKEND', 
            default='django.core.cache.backends.locmem.LocMemCache'
        ),
        'LOCATION': config('CACHE_LOCATION', default=''),
        'TIMEOUT': config('CACHE_TIMEOUT', default=300, cast=int),
        'OPTIONS': {
            'MAX_ENTRIES': config('CACHE_MAX_ENTRIES', default=1000, cast=int),
        }
    }
}

# Logging para produção
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
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': config('LOG_FILE', default='django_prod.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Email para produção
if config('EMAIL_BACKEND', default='') == 'smtp':
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@encanointimo.com')

# Configurações específicas para ambiente de produção
ADMINS = [
    ('Admin', config('ADMIN_EMAIL', default='admin@encanointimo.com')),
]

MANAGERS = ADMINS

# Timeout de sessão (30 minutos)
SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE', default=1800, cast=int)

# Configurações de arquivo estático para produção
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = config('STATIC_ROOT', default='staticfiles')

# Media files para produção
MEDIA_ROOT = config('MEDIA_ROOT', default='media')
