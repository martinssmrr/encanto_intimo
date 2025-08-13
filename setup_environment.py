#!/usr/bin/env python3
"""
Script de setup para o projeto Encanto Íntimo
Facilita a configuração inicial dos ambientes de desenvolvimento e produção.
"""

import os
import sys
import shutil
from pathlib import Path

def create_env_file(environment='dev'):
    """Cria arquivo .env baseado no ambiente"""
    
    env_templates = {
        'dev': """# Configurações de Desenvolvimento - Encanto Íntimo
SECRET_KEY=django-insecure-dev-key-substitua-em-producao
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Email (Console backend para desenvolvimento)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Stripe - Chaves de teste
STRIPE_TEST_PUBLISHABLE_KEY=pk_test_seu_publishable_key
STRIPE_TEST_SECRET_KEY=sk_test_seu_secret_key

# MercadoPago - Chaves de teste
MERCADOPAGO_TEST_ACCESS_TOKEN=TEST-seu-access-token
MERCADOPAGO_TEST_PUBLIC_KEY=TEST-seu-public-key

# Admin
ADMIN_EMAIL=admin@encantointimo.local
""",
        
        'prod': """# Configurações de Produção - Encanto Íntimo
# IMPORTANTE: Configure todas as variáveis antes do deploy!

SECRET_KEY=SUBSTITUA-POR-UMA-CHAVE-FORTE-E-SEGURA
DEBUG=False
ALLOWED_HOSTS=encantointimo.com,www.encantointimo.com

# Database PostgreSQL
DB_NAME=encanto_intimo_prod
DB_USER=encanto_user
DB_PASSWORD=SUBSTITUA-POR-SENHA-FORTE
DB_HOST=localhost
DB_PORT=5432

# Email SMTP
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app
DEFAULT_FROM_EMAIL=noreply@encantointimo.com

# Stripe - Chaves de produção
STRIPE_LIVE_PUBLISHABLE_KEY=pk_live_SUBSTITUA
STRIPE_LIVE_SECRET_KEY=sk_live_SUBSTITUA

# MercadoPago - Chaves de produção
MERCADOPAGO_LIVE_ACCESS_TOKEN=APP_USR-SUBSTITUA
MERCADOPAGO_LIVE_PUBLIC_KEY=APP_USR-SUBSTITUA

# Redis para cache
REDIS_URL=redis://127.0.0.1:6379/1

# AWS S3 (opcional)
USE_S3=False
AWS_ACCESS_KEY_ID=sua_access_key
AWS_SECRET_ACCESS_KEY=sua_secret_key
AWS_STORAGE_BUCKET_NAME=encanto-intimo-bucket
AWS_S3_REGION_NAME=us-east-1

# Monitoramento (opcional)
SENTRY_DSN=https://seu_dsn@sentry.io/projeto

# Admin
ADMIN_EMAIL=admin@encantointimo.com
"""
    }
    
    filename = f'.env.{environment}' if environment != 'dev' else '.env'
    
    if os.path.exists(filename):
        response = input(f"Arquivo {filename} já existe. Sobrescrever? (y/N): ")
        if response.lower() != 'y':
            print(f"✅ Mantendo arquivo {filename} existente")
            return
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(env_templates[environment])
    
    print(f"✅ Arquivo {filename} criado com sucesso!")
    if environment == 'prod':
        print("⚠️  IMPORTANTE: Configure todas as variáveis antes de usar em produção!")

def create_log_directory():
    """Cria diretório de logs"""
    log_dir = Path('logs')
    if not log_dir.exists():
        log_dir.mkdir()
        print("✅ Diretório 'logs' criado")
        
        # Criar .gitignore para logs
        with open(log_dir / '.gitignore', 'w') as f:
            f.write("*.log\n")
        print("✅ .gitignore criado no diretório logs")
    else:
        print("ℹ️  Diretório 'logs' já existe")

def check_requirements():
    """Verifica se todas as dependências estão instaladas"""
    required_packages = [
        'django',
        'python-decouple',
        'Pillow',
        'django-crispy-forms',
        'crispy-tailwind',
        'django-widget-tweaks'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Pacotes faltando:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Execute: pip install -r requirements.txt")
        return False
    else:
        print("✅ Todas as dependências estão instaladas")
        return True

def run_initial_setup():
    """Executa configuração inicial"""
    print("🚀 Executando configuração inicial...")
    
    # Criar migrações
    os.system('python manage.py makemigrations')
    
    # Aplicar migrações
    os.system('python manage.py migrate')
    
    # Coletar arquivos estáticos
    os.system('python manage.py collectstatic --noinput')
    
    print("✅ Configuração inicial concluída!")

def main():
    """Função principal"""
    print("=" * 60)
    print("🎉 SETUP DO PROJETO ENCANTO ÍNTIMO")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        environment = sys.argv[1]
        if environment not in ['dev', 'prod']:
            print("❌ Ambiente deve ser 'dev' ou 'prod'")
            sys.exit(1)
    else:
        print("\nEscolha o ambiente:")
        print("1. Desenvolvimento (dev)")
        print("2. Produção (prod)")
        choice = input("\nDigite sua escolha (1 ou 2): ")
        
        if choice == '1':
            environment = 'dev'
        elif choice == '2':
            environment = 'prod'
        else:
            print("❌ Escolha inválida")
            sys.exit(1)
    
    print(f"\n🔧 Configurando ambiente: {environment.upper()}")
    print("-" * 40)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('manage.py'):
        print("❌ Execute este script a partir do diretório raiz do projeto")
        sys.exit(1)
    
    # Criar diretório de logs
    create_log_directory()
    
    # Criar arquivo .env
    create_env_file(environment)
    
    if environment == 'dev':
        # Verificar dependências
        if check_requirements():
            setup = input("\n🤔 Executar configuração inicial? (migrate, collectstatic) (Y/n): ")
            if setup.lower() != 'n':
                run_initial_setup()
        
        print("\n" + "=" * 60)
        print("✅ SETUP DE DESENVOLVIMENTO CONCLUÍDO!")
        print("=" * 60)
        print("\n📋 Próximos passos:")
        print("1. Configure as variáveis no arquivo .env")
        print("2. Execute: python manage.py runserver")
        print("3. Acesse: http://127.0.0.1:8000")
        
    else:  # prod
        print("\n" + "=" * 60)
        print("✅ ARQUIVOS DE PRODUÇÃO CRIADOS!")
        print("=" * 60)
        print("\n📋 Próximos passos para produção:")
        print("1. ⚠️  Configure TODAS as variáveis no .env.prod")
        print("2. Configure PostgreSQL")
        print("3. Configure servidor web (Nginx/Apache)")
        print("4. Execute: export DJANGO_SETTINGS_MODULE=encanto_intimo.settings.prod")
        print("5. Execute: python manage.py migrate")
        print("6. Execute: python manage.py collectstatic")
        print("7. Execute: gunicorn encanto_intimo.wsgi:application")
        
    print(f"\n📚 Consulte CONFIGURACOES.md para mais informações")

if __name__ == '__main__':
    main()
