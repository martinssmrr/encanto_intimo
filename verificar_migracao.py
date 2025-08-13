#!/usr/bin/env python
"""
Script de Verificação Pós-Migração MySQL
Projeto: Encanto Íntimo

Verifica se a migração SQLite → MySQL foi bem-sucedida:
1. Testa conexão com MySQL
2. Verifica se todas as tabelas foram criadas
3. Testa funcionalidades básicas
4. Valida configurações de segurança

Uso:
    python verificar_migracao.py
"""

import os
import sys
import django
from decouple import config

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
django.setup()

from django.db import connection
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test.utils import override_settings
import mysql.connector
from mysql.connector import Error

def print_header(title):
    """Imprime cabeçalho formatado"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"❌ {message}")

def print_info(message):
    """Imprime mensagem informativa"""
    print(f"ℹ️  {message}")

def test_mysql_connection():
    """Testa conexão direta com MySQL"""
    print_header("TESTE DE CONEXÃO MYSQL")
    
    try:
        # Conexão usando as configurações do Django
        db_config = {
            'host': config('DB_HOST', default='localhost'),
            'port': config('DB_PORT', default='3306', cast=int),
            'user': config('DB_USER', default='encanto_admin'),
            'password': config('DB_PASSWORD'),
            'database': config('DB_NAME', default='db_encanto'),
            'charset': 'utf8mb4'
        }
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Teste básico
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print_success(f"MySQL conectado! Versão: {version[0]}")
        
        # Verificar charset
        cursor.execute("SELECT @@character_set_database, @@collation_database")
        charset_info = cursor.fetchone()
        print_success(f"Charset: {charset_info[0]}, Collation: {charset_info[1]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Error as e:
        print_error(f"Erro na conexão MySQL: {e}")
        return False

def test_django_connection():
    """Testa conexão Django com MySQL"""
    print_header("TESTE DE CONEXÃO DJANGO")
    
    try:
        # Testar conexão Django
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result and result[0] == 1:
            print_success("Conexão Django → MySQL funcionando!")
            
            # Informações da conexão
            db_info = connection.settings_dict
            print_info(f"Engine: {db_info['ENGINE']}")
            print_info(f"Database: {db_info['NAME']}")
            print_info(f"Host: {db_info['HOST']}:{db_info['PORT']}")
            print_info(f"User: {db_info['USER']}")
            
            return True
        else:
            print_error("Teste de conexão Django falhou!")
            return False
            
    except Exception as e:
        print_error(f"Erro na conexão Django: {e}")
        return False

def check_tables():
    """Verifica se todas as tabelas foram criadas"""
    print_header("VERIFICAÇÃO DE TABELAS")
    
    try:
        cursor = connection.cursor()
        
        # Listar todas as tabelas
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        print_success(f"Total de tabelas encontradas: {len(tables)}")
        
        # Tabelas essenciais que devem existir
        essential_tables = [
            'auth_user',
            'django_session',
            'django_site',
            'django_content_type',
            'usuarios_perfilusuario',
            'produtos_produto',
            'produtos_categoria',
            'carrinho_carrinho',
            'pedidos_pedido',
            'account_emailaddress',
            'socialaccount_socialaccount'
        ]
        
        missing_tables = []
        for table in essential_tables:
            if table in tables:
                print_success(f"Tabela {table}: OK")
            else:
                missing_tables.append(table)
                print_error(f"Tabela {table}: FALTANDO")
        
        if missing_tables:
            print_error(f"Tabelas faltando: {missing_tables}")
            return False
        else:
            print_success("Todas as tabelas essenciais estão presentes!")
            return True
            
    except Exception as e:
        print_error(f"Erro ao verificar tabelas: {e}")
        return False

def test_basic_operations():
    """Testa operações básicas do Django"""
    print_header("TESTE DE OPERAÇÕES BÁSICAS")
    
    try:
        # Testar contagem de usuários
        user_count = User.objects.count()
        print_success(f"Usuários no sistema: {user_count}")
        
        # Testar criação/leitura (sem commit)
        from django.db import transaction
        
        with transaction.atomic():
            # Criar usuário de teste
            test_user = User.objects.create_user(
                username='test_migration_user',
                email='test@migracao.com',
                password='teste123'
            )
            print_success("Criação de usuário: OK")
            
            # Ler usuário
            found_user = User.objects.get(username='test_migration_user')
            print_success(f"Leitura de usuário: OK (ID: {found_user.id})")
            
            # Rollback para não salvar o usuário de teste
            raise transaction.TransactionManagementError("Rollback intencional")
            
    except transaction.TransactionManagementError:
        print_success("Operações básicas funcionando (rollback executado)")
        return True
    except Exception as e:
        print_error(f"Erro nas operações básicas: {e}")
        return False

def check_security_settings():
    """Verifica configurações de segurança"""
    print_header("VERIFICAÇÃO DE SEGURANÇA")
    
    try:
        from django.conf import settings
        
        # Verificar configurações importantes
        security_checks = [
            ("SECRET_KEY definida", bool(settings.SECRET_KEY and len(settings.SECRET_KEY) > 30)),
            ("DEBUG mode", settings.DEBUG),  # True em dev é OK
            ("ALLOWED_HOSTS configurado", bool(settings.ALLOWED_HOSTS)),
            ("MySQL em uso", 'mysql' in settings.DATABASES['default']['ENGINE']),
            ("Charset UTF8MB4", settings.DATABASES['default']['OPTIONS'].get('charset') == 'utf8mb4'),
            ("Middleware de segurança", 'django.middleware.security.SecurityMiddleware' in settings.MIDDLEWARE),
            ("CSRF Protection", 'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE),
        ]
        
        all_ok = True
        for check_name, result in security_checks:
            if result:
                print_success(f"{check_name}: ✓")
            else:
                print_error(f"{check_name}: ✗")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print_error(f"Erro na verificação de segurança: {e}")
        return False

def check_apps_functionality():
    """Verifica se os apps estão funcionando"""
    print_header("VERIFICAÇÃO DE APPS")
    
    try:
        from django.apps import apps
        
        # Apps essenciais do projeto
        project_apps = [
            'usuarios',
            'produtos', 
            'carrinho',
            'pedidos',
            'fornecedores',
            'pagamentos'
        ]
        
        all_ok = True
        for app_name in project_apps:
            try:
                app = apps.get_app_config(app_name)
                models = app.get_models()
                print_success(f"App {app_name}: {len(models)} modelos carregados")
            except Exception as e:
                print_error(f"App {app_name}: Erro - {e}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print_error(f"Erro na verificação de apps: {e}")
        return False

def main():
    """Executa todas as verificações"""
    print_header("VERIFICAÇÃO COMPLETA DA MIGRAÇÃO MYSQL")
    print("🔍 Verificando se a migração SQLite → MySQL foi bem-sucedida...\n")
    
    # Lista de testes
    tests = [
        ("Conexão MySQL Direta", test_mysql_connection),
        ("Conexão Django", test_django_connection), 
        ("Estrutura de Tabelas", check_tables),
        ("Operações Básicas", test_basic_operations),
        ("Configurações de Segurança", check_security_settings),
        ("Funcionalidade de Apps", check_apps_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Executando: {test_name}")
        result = test_func()
        results.append((test_name, result))
    
    # Resumo final
    print_header("RESUMO DA VERIFICAÇÃO")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    print(f"\n📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("✅ Todos os testes passaram")
        print("✅ Sistema MySQL funcionando perfeitamente")
        print("✅ Pronto para uso em desenvolvimento")
        print("\n💡 Próximos passos:")
        print("   1. Teste todas as funcionalidades na interface")
        print("   2. Execute: python manage.py runserver")
        print("   3. Acesse: http://localhost:8000")
    else:
        print("\n⚠️  ALGUNS PROBLEMAS ENCONTRADOS")
        print("🔧 Verifique os erros acima e corrija antes de usar")
        
        failed_tests = [name for name, result in results if not result]
        print(f"❌ Testes que falharam: {', '.join(failed_tests)}")

if __name__ == "__main__":
    main()
