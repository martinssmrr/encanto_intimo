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
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            # Configurações SSL apenas em produção
            'ssl': config('DB_SSL_ENABLED', default=False, cast=bool),
            'ssl_ca': config('DB_SSL_CA', default=None),
        },
        'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=300, cast=int),  # 5 minutos para produção
        'CONN_HEALTH_CHECKS': True,
    }
}

# ============================================================================
# CONFIGURAÇÕES DE SEGURANÇA PARA PRODUÇÃO
# ============================================================================

# SSL/HTTPS obrigatório em produção
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 ano
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Política de referrer restrita
SECURE_REFERRER_POLICY = "strict-origin"

# Proteções de cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Proteção contra ataques de content-type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Proteção XSS
SECURE_BROWSER_XSS_FILTER = True

# Proteção contra clickjacking
X_FRAME_OPTIONS = 'DENY'

# Proxy headers (para uso com load balancers)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# ============================================================================
# CONFIGURAÇÕES DE ARQUIVOS ESTÁTICOS E MÍDIA PARA PRODUÇÃO
# ============================================================================

# Static files para produção (AWS S3 ou CDN)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuração para AWS S3 (se usar)
if config('USE_S3', default=False, cast=bool):
    # AWS S3 Settings
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # Static files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    
    # Media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# ============================================================================
# CONFIGURAÇÕES DE CACHE PARA PRODUÇÃO
# ============================================================================

# Redis cache para produção
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'encanto_intimo',
        'TIMEOUT': 300,  # 5 minutos padrão
    }
}

# Cache de sessões no Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# ============================================================================
# CONFIGURAÇÕES DE EMAIL PARA PRODUÇÃO
# ============================================================================

# Email backend para produção
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@encantointimo.com')

# ============================================================================
# CONFIGURAÇÕES DE LOGGING PARA PRODUÇÃO
# ============================================================================

# Configuração avançada de logging para produção
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
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/encanto_intimo/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/encanto_intimo/error.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'encanto_intimo': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================================================
# CONFIGURAÇÕES DE ADMINISTRAÇÃO
# ============================================================================

ADMINS = [
    ('Admin Encanto Íntimo', config('ADMIN_EMAIL', default='admin@encantointimo.com')),
]

MANAGERS = ADMINS

# ============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================================================

# Compressão GZIP
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
] + MIDDLEWARE

# Configurações de timezone
USE_TZ = True

# ============================================================================
# CONFIGURAÇÕES DE PAGAMENTO PARA PRODUÇÃO
# ============================================================================

# Stripe - Chaves de produção
STRIPE_PUBLISHABLE_KEY = config('STRIPE_LIVE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_LIVE_SECRET_KEY')

# MercadoPago - Chaves de produção
MERCADOPAGO_ACCESS_TOKEN = config('MERCADOPAGO_LIVE_ACCESS_TOKEN')
MERCADOPAGO_PUBLIC_KEY = config('MERCADOPAGO_LIVE_PUBLIC_KEY')

# ============================================================================
# CONFIGURAÇÕES DE MONITORAMENTO
# ============================================================================

# Sentry para monitoramento de erros (opcional)
SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), sentry_logging],
        traces_sample_rate=0.1,
        send_default_pii=True,
        environment='production',
    )

# ============================================================================
# CONFIGURAÇÕES FINAIS
# ============================================================================

# Desabilitar browsable API em produção (se usar DRF)
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# Força coleta de lixo mais frequente em produção
import gc
gc.set_threshold(700, 10, 10)

print("🏭 Executando em modo PRODUÇÃO")
print(f"🔒 SSL Redirect: {SECURE_SSL_REDIRECT}")
print(f"🗄️  Database: PostgreSQL")
print(f"📧 Email: SMTP")
print(f"🔧 Debug: {DEBUG}")
print("⚠️  ATENÇÃO: Verifique todas as variáveis de ambiente!")
