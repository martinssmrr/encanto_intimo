"""
Configurações de desenvolvimento para o projeto Encanto Íntimo.

Este arquivo contém configurações específicas para o ambiente de desenvolvimento,
incluindo DEBUG=True, banco de dados local e ferramentas de debug.
"""

from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Hosts permitidos em desenvolvimento
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '192.168.1.*',  # Para testes em rede local
]

# Database para desenvolvimento
# MySQL configurado para desenvolvimento local
DATABASES = {
    "default": {
        "ENGINE": config('DB_ENGINE', default='django.db.backends.mysql'),
        "NAME": config('DB_NAME', default='db_encanto'),
        "USER": config('DB_USER', default='encanto_admin'),
        "PASSWORD": config('DB_PASSWORD', default=''),
        "HOST": config('DB_HOST', default='localhost'),
        "PORT": config('DB_PORT', default='3306'),
        "OPTIONS": {
            'charset': 'utf8mb4',
            # Configurações mínimas para desenvolvimento
        },
        'CONN_MAX_AGE': 60,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Static files para desenvolvimento
STATIC_ROOT = BASE_DIR / "staticfiles"

# Email backend para desenvolvimento
# Console backend mostra emails no terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Configurações de cache para desenvolvimento
# Cache em memória local para testes
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'encanto-intimo-dev-cache',
    }
}

# Session configuration para desenvolvimento
SESSION_COOKIE_SECURE = False  # HTTP é permitido em desenvolvimento
CSRF_COOKIE_SECURE = False     # HTTP é permitido em desenvolvimento

# Configurações específicas para desenvolvimento
# Desabilitar algumas verificações de segurança em desenvolvimento
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False

# Middleware adicional para desenvolvimento
# Django Debug Toolbar (se instalado)
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ['debug_toolbar']
        MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
        DEBUG_TOOLBAR_CONFIG = {
            'SHOW_TOOLBAR_CALLBACK': lambda request: True,
        }
        INTERNAL_IPS = [
            '127.0.0.1',
            'localhost',
        ]
    except ImportError:
        pass

# Logging configuration para desenvolvimento
LOGGING['handlers']['file_dev'] = {
    'level': 'DEBUG',
    'class': 'logging.FileHandler',
    'filename': BASE_DIR / 'logs' / 'dev.log',
    'formatter': 'verbose',
}

LOGGING['loggers']['encanto_intimo']['handlers'] = ['console', 'file_dev']
LOGGING['loggers']['encanto_intimo']['level'] = 'DEBUG'

# Criar diretório de logs se não existir
import os
log_dir = BASE_DIR / 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurações para desenvolvimento de pagamentos
# Usar chaves de teste do Stripe
STRIPE_PUBLISHABLE_KEY = config('STRIPE_TEST_PUBLISHABLE_KEY', default='pk_test_...')
STRIPE_SECRET_KEY = config('STRIPE_TEST_SECRET_KEY', default='sk_test_...')

# Configurações específicas do Django em desenvolvimento
ADMINS = [
    ('Desenvolvedor', 'dev@encantointimo.com'),
]

MANAGERS = ADMINS

# Configuração para arquivo de mídia em desenvolvimento
# Permitir acesso a arquivos de mídia via Django
if DEBUG:
    from django.conf.urls.static import static
    from django.urls import include, re_path
    
    # Esta configuração será automaticamente incluída pelo urls.py principal

# Configurações de performance para desenvolvimento
# Em desenvolvimento, não precisamos de otimizações agressivas
USE_TZ = True
USE_L10N = True

# Configurações de template para desenvolvimento
# Recarregar templates automaticamente
TEMPLATES[0]['OPTIONS']['debug'] = True

print("🚀 Executando em modo DESENVOLVIMENTO")
print(f"📁 BASE_DIR: {BASE_DIR}")
print(f"🗄️  Database: SQLite (db.sqlite3)")
print(f"📧 Email: Console Backend")
print(f"🔧 Debug: {DEBUG}")
