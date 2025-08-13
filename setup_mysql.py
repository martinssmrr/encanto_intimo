#!/usr/bin/env python
"""
Script para configurar o banco de dados MySQL para o projeto Encanto Íntimo.

Este script:
1. Testa a conexão com o MySQL
2. Cria o banco de dados se não existir
3. Configura o usuário e permissões
4. Executa as migrações iniciais

Uso:
    python setup_mysql.py

Pré-requisitos:
    - MySQL Server instalado e rodando
    - Root access ao MySQL ou usuário com privilégios administrativos
    - Credenciais configuradas no .env
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from decouple import config
import mysql.connector
from mysql.connector import Error

def teste_conexao_mysql():
    """Testa a conexão básica com o MySQL"""
    try:
        print("🔍 Testando conexão com MySQL...")
        
        # Conecta ao MySQL sem especificar banco
        connection = mysql.connector.connect(
            host=config('DB_HOST', default='localhost'),
            port=config('DB_PORT', default=3306, cast=int),
            user='root',  # Usamos root para configuração inicial
            password=input("Digite a senha do root do MySQL: ")
        )
        
        if connection.is_connected():
            print("✅ Conexão com MySQL estabelecida com sucesso!")
            return connection
        
    except Error as e:
        print(f"❌ Erro ao conectar com MySQL: {e}")
        return None

def criar_banco_e_usuario(connection):
    """Cria o banco de dados e usuário se não existirem"""
    try:
        cursor = connection.cursor()
        
        # Configurações do .env
        db_name = config('DB_NAME', default='db_encanto')
        db_user = config('DB_USER', default='encanto_admin')
        db_password = config('DB_PASSWORD', default='Marrequeiro3750@')
        db_host = config('DB_HOST', default='localhost')
        
        print(f"🏗️ Configurando banco: {db_name}")
        print(f"👤 Usuário: {db_user}")
        
        # Criar banco de dados
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"✅ Banco de dados '{db_name}' criado/verificado")
        
        # Criar usuário
        cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'{db_host}' IDENTIFIED BY '{db_password}';")
        print(f"✅ Usuário '{db_user}' criado/verificado")
        
        # Conceder privilégios
        cursor.execute(f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'{db_host}';")
        cursor.execute("FLUSH PRIVILEGES;")
        print(f"✅ Privilégios concedidos ao usuário '{db_user}'")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False

def testar_conexao_django():
    """Testa a conexão usando as configurações do Django"""
    try:
        print("🔍 Testando conexão Django com MySQL...")
        
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
        django.setup()
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("✅ Conexão Django com MySQL funcionando!")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão Django: {e}")
        return False

def executar_migracoes():
    """Executa as migrações do Django"""
    try:
        print("🔄 Executando migrações...")
        
        # Definir settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
        
        # Executar migrações
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrações executadas com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Configuração do MySQL para Encanto Íntimo")
    print("=" * 50)
    
    # Testar conexão MySQL
    connection = teste_conexao_mysql()
    if not connection:
        print("❌ Não foi possível conectar ao MySQL. Verifique se o MySQL está rodando.")
        return
    
    # Criar banco e usuário
    if not criar_banco_e_usuario(connection):
        connection.close()
        return
    
    connection.close()
    
    # Testar conexão Django
    if not testar_conexao_django():
        print("❌ Falha na conexão Django. Verifique as configurações no .env")
        return
    
    # Executar migrações
    if not executar_migracoes():
        print("❌ Falha ao executar migrações")
        return
    
    print("\n🎉 Configuração MySQL concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Execute: python manage.py createsuperuser")
    print("2. Execute: python manage.py runserver")
    print("3. Acesse: http://localhost:8000")

if __name__ == "__main__":
    main()
