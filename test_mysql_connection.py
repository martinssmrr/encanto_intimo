#!/usr/bin/env python
"""
Script para testar a conexão MySQL do projeto Encanto Íntimo.

Este script verifica:
1. Conectividade básica com MySQL
2. Configurações do Django
3. Migrações aplicadas
4. Integridade dos dados

Uso:
    python test_mysql_connection.py
"""

import os
import sys
import django
from decouple import config

def testar_configuracoes_env():
    """Testa se as configurações do .env estão corretas"""
    print("🔍 Verificando configurações do .env...")
    
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']
    missing_vars = []
    
    for var in required_vars:
        value = config(var, default=None)
        if not value:
            missing_vars.append(var)
        else:
            # Mascarar senha na saída
            if var == 'DB_PASSWORD':
                print(f"✅ {var}: {'*' * len(value)}")
            else:
                print(f"✅ {var}: {value}")
    
    if missing_vars:
        print(f"❌ Variáveis faltando no .env: {missing_vars}")
        return False
    
    return True

def testar_mysql_direto():
    """Testa conexão direta com MySQL"""
    try:
        import mysql.connector
        from mysql.connector import Error
        
        print("🔍 Testando conexão direta com MySQL...")
        
        connection = mysql.connector.connect(
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default=3306, cast=int),
            user=config('DB_USER', default='encanto_admin'),
            password=config('DB_PASSWORD', default=''),
            database=config('DB_NAME', default='db_encanto')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL conectado! Versão: {version[0]}")
            
            # Testar charset
            cursor.execute("SELECT @@character_set_database, @@collation_database")
            charset_info = cursor.fetchone()
            print(f"✅ Charset: {charset_info[0]}, Collation: {charset_info[1]}")
            
            cursor.close()
            connection.close()
            return True
            
    except ImportError:
        print("⚠️ mysql-connector-python não está instalado")
        print("   Tentando com mysqlclient...")
        return True  # Continuar com Django
        
    except Error as e:
        print(f"❌ Erro na conexão MySQL: {e}")
        return False

def testar_django_mysql():
    """Testa conexão Django com MySQL"""
    try:
        print("🔍 Testando conexão Django com MySQL...")
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
        django.setup()
        
        from django.db import connection
        from django.core.management import call_command
        
        # Testar conexão
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("✅ Django conectado ao MySQL!")
            
            # Informações da conexão
            db_info = connection.get_connection_params()
            print(f"✅ Banco: {db_info.get('database', 'N/A')}")
            print(f"✅ Host: {db_info.get('host', 'N/A')}")
            print(f"✅ Porta: {db_info.get('port', 'N/A')}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão Django: {e}")
        return False

def verificar_migracoes():
    """Verifica status das migrações"""
    try:
        print("🔍 Verificando migrações...")
        
        from django.core.management import call_command
        from io import StringIO
        import sys
        
        # Capturar saída do comando
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            call_command('showmigrations', '--plan')
            output = sys.stdout.getvalue()
        finally:
            sys.stdout = old_stdout
        
        # Contar migrações
        lines = output.strip().split('\n')
        applied = len([line for line in lines if '[X]' in line])
        total = len([line for line in lines if '[' in line])
        
        print(f"✅ Migrações: {applied}/{total} aplicadas")
        
        if applied < total:
            print("⚠️ Existem migrações pendentes!")
            print("   Execute: python manage.py migrate")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar migrações: {e}")
        return False

def verificar_tabelas():
    """Verifica se as tabelas principais existem"""
    try:
        print("🔍 Verificando tabelas...")
        
        from django.db import connection
        
        # Lista de tabelas esperadas
        expected_tables = [
            'auth_user',
            'django_session',
            'django_migrations',
            'usuarios_perfilusuario',
            'produtos_produto',
            'produtos_categoria',
            'pedidos_pedido',
            'carrinho_carrinho'
        ]
        
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        found_tables = []
        missing_tables = []
        
        for table in expected_tables:
            if table in existing_tables:
                found_tables.append(table)
            else:
                missing_tables.append(table)
        
        print(f"✅ Tabelas encontradas: {len(found_tables)}")
        for table in found_tables:
            print(f"   ✓ {table}")
        
        if missing_tables:
            print(f"⚠️ Tabelas faltando: {len(missing_tables)}")
            for table in missing_tables:
                print(f"   ✗ {table}")
        
        return len(missing_tables) == 0
        
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return False

def testar_operacoes_basicas():
    """Testa operações básicas no banco"""
    try:
        print("🔍 Testando operações básicas...")
        
        from django.contrib.auth.models import User
        from django.db import transaction
        
        # Testar consulta
        user_count = User.objects.count()
        print(f"✅ Consulta: {user_count} usuários encontrados")
        
        # Testar transação (sem commit)
        with transaction.atomic():
            # Criar usuário temporário
            test_user = User(
                username=f'test_user_temp',
                email='test@test.com'
            )
            test_user.save()
            
            # Verificar se foi salvo
            exists = User.objects.filter(username='test_user_temp').exists()
            print(f"✅ Transação: usuário temporário {'criado' if exists else 'não criado'}")
            
            # Reverter transação
            raise Exception("Rollback intencional")
        
    except Exception as e:
        if "Rollback intencional" in str(e):
            print("✅ Rollback: transação revertida com sucesso")
            return True
        else:
            print(f"❌ Erro em operações básicas: {e}")
            return False

def main():
    """Função principal"""
    print("🔍 Teste de Conexão MySQL - Encanto Íntimo")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 6
    
    # Teste 1: Configurações .env
    if testar_configuracoes_env():
        tests_passed += 1
    print()
    
    # Teste 2: Conexão MySQL direta
    if testar_mysql_direto():
        tests_passed += 1
    print()
    
    # Teste 3: Conexão Django
    if testar_django_mysql():
        tests_passed += 1
    print()
    
    # Teste 4: Migrações
    if verificar_migracoes():
        tests_passed += 1
    print()
    
    # Teste 5: Tabelas
    if verificar_tabelas():
        tests_passed += 1
    print()
    
    # Teste 6: Operações básicas
    if testar_operacoes_basicas():
        tests_passed += 1
    print()
    
    # Resultado final
    print("=" * 50)
    print(f"📊 Resultado: {tests_passed}/{total_tests} testes passaram")
    
    if tests_passed == total_tests:
        print("🎉 Todos os testes passaram! MySQL configurado corretamente.")
        print("\n📋 Próximos passos:")
        print("1. Execute: python manage.py runserver")
        print("2. Acesse: http://localhost:8000")
    else:
        print("❌ Alguns testes falharam. Verifique as mensagens acima.")
        print("\n🔧 Possíveis soluções:")
        print("1. Verificar se MySQL está rodando")
        print("2. Verificar credenciais no .env")
        print("3. Executar: python setup_mysql.py")
        print("4. Executar: python manage.py migrate")

if __name__ == "__main__":
    main()
