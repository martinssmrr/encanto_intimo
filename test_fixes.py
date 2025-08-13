#!/usr/bin/env python
"""
Script simples para testar a configuração corrigida do MySQL.

Este script verifica se os problemas foram resolvidos:
1. Warning do django-allauth
2. Erro de privilégios MySQL
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def testar_configuracoes():
    """Testa as configurações corrigidas"""
    print("🔍 Testando configurações corrigidas...")
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
    
    try:
        django.setup()
        print("✅ Django configurado com sucesso!")
        
        # Testar conexão com banco
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result:
            print("✅ Conexão MySQL funcionando!")
            
            # Testar se consegue verificar migrações
            from django.core.management import call_command
            from io import StringIO
            import sys
            
            # Capturar output
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            
            try:
                call_command('check')
                stdout_output = sys.stdout.getvalue()
                stderr_output = sys.stderr.getvalue()
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
            
            if 'ACCOUNT_LOGIN_METHODS conflicts' in stderr_output:
                print("❌ Warning allauth ainda presente")
                print(f"   Detalhes: {stderr_output}")
            else:
                print("✅ Warning allauth corrigido!")
            
            if 'SYSTEM_VARIABLES_ADMIN' in stderr_output:
                print("❌ Erro MySQL ainda presente")
                print(f"   Detalhes: {stderr_output}")
            else:
                print("✅ Erro MySQL corrigido!")
            
            return True
            
    except Exception as e:
        error_msg = str(e)
        
        if 'SYSTEM_VARIABLES_ADMIN' in error_msg:
            print("❌ Erro MySQL ainda presente:")
            print(f"   {error_msg}")
            print("\n🔧 Solução:")
            print("   1. Verifique se o usuário MySQL tem as permissões corretas")
            print("   2. Execute o script setup_mysql.py novamente")
            print("   3. Ou conecte-se como root e execute:")
            print("      GRANT ALL PRIVILEGES ON db_encanto.* TO 'encanto_admin'@'localhost';")
            
        elif 'ACCOUNT_LOGIN_METHODS' in error_msg:
            print("❌ Warning allauth ainda presente:")
            print(f"   {error_msg}")
            
        else:
            print(f"❌ Outro erro encontrado: {error_msg}")
        
        return False

def main():
    """Função principal"""
    print("🧪 Teste de Correções - Encanto Íntimo")
    print("=" * 40)
    
    if testar_configuracoes():
        print("\n🎉 Todos os problemas foram corrigidos!")
        print("\n📋 Próximos passos:")
        print("1. Execute: python manage.py migrate")
        print("2. Execute: python manage.py runserver")
    else:
        print("\n⚠️ Alguns problemas ainda precisam ser resolvidos.")

if __name__ == "__main__":
    main()
