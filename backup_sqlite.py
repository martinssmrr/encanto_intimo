#!/usr/bin/env python
"""
Script para fazer backup dos dados do SQLite antes da migração para MySQL.

Este script:
1. Cria um backup dos dados existentes no SQLite
2. Exporta dados para fixtures JSON
3. Salva cópia do banco SQLite

Uso:
    python backup_sqlite.py
"""

import os
import sys
import django
from django.core.management import call_command
from datetime import datetime
import shutil

def configurar_django():
    """Configura o Django para usar SQLite temporariamente"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
    
    # Temporariamente usar SQLite para backup
    os.environ['DB_ENGINE'] = 'django.db.backends.sqlite3'
    os.environ['DB_NAME'] = 'db.sqlite3'
    
    django.setup()

def verificar_sqlite():
    """Verifica se o banco SQLite existe"""
    sqlite_path = 'db.sqlite3'
    
    if not os.path.exists(sqlite_path):
        print("ℹ️ Nenhum banco SQLite encontrado. Nada para fazer backup.")
        return False
    
    print(f"📂 Banco SQLite encontrado: {sqlite_path}")
    return True

def criar_backup_arquivo():
    """Cria uma cópia do arquivo SQLite"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"backup_sqlite_{timestamp}.db"
        
        shutil.copy2('db.sqlite3', backup_filename)
        print(f"✅ Backup do arquivo criado: {backup_filename}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar backup do arquivo: {e}")
        return False

def exportar_dados():
    """Exporta dados para fixtures JSON"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Lista de apps para fazer backup
        apps = [
            'usuarios',
            'produtos', 
            'pedidos',
            'carrinho',
            'fornecedores',
            'pagamentos'
        ]
        
        backup_dir = f"backup_data_{timestamp}"
        os.makedirs(backup_dir, exist_ok=True)
        
        print("📦 Exportando dados...")
        
        for app in apps:
            try:
                fixture_file = os.path.join(backup_dir, f"{app}_data.json")
                call_command('dumpdata', app, format='json', indent=2, output=fixture_file)
                print(f"✅ {app}: dados exportados para {fixture_file}")
                
            except Exception as e:
                print(f"⚠️ {app}: {e}")
        
        # Backup dos dados de autenticação
        try:
            auth_file = os.path.join(backup_dir, "auth_data.json")
            call_command('dumpdata', 'auth.User', 'auth.Group', format='json', indent=2, output=auth_file)
            print(f"✅ auth: dados exportados para {auth_file}")
        except Exception as e:
            print(f"⚠️ auth: {e}")
        
        # Backup dos sites (para allauth)
        try:
            sites_file = os.path.join(backup_dir, "sites_data.json")
            call_command('dumpdata', 'sites', format='json', indent=2, output=sites_file)
            print(f"✅ sites: dados exportados para {sites_file}")
        except Exception as e:
            print(f"⚠️ sites: {e}")
        
        print(f"📁 Todos os dados exportados para: {backup_dir}")
        return backup_dir
        
    except Exception as e:
        print(f"❌ Erro ao exportar dados: {e}")
        return None

def criar_script_restauracao(backup_dir):
    """Cria script para restaurar dados no MySQL"""
    script_content = f"""#!/usr/bin/env python
\"\"\"
Script para restaurar dados no MySQL após migração.

Gerado automaticamente em {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
\"\"\"

import os
import django
from django.core.management import call_command

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
    django.setup()
    
    print("🔄 Restaurando dados no MySQL...")
    
    # Lista de arquivos para carregar (ordem importa!)
    fixtures = [
        'sites_data.json',
        'auth_data.json',
        'usuarios_data.json',
        'fornecedores_data.json',
        'produtos_data.json',
        'pedidos_data.json',
        'carrinho_data.json',
        'pagamentos_data.json'
    ]
    
    backup_dir = '{backup_dir}'
    
    for fixture in fixtures:
        fixture_path = os.path.join(backup_dir, fixture)
        
        if os.path.exists(fixture_path):
            try:
                call_command('loaddata', fixture_path)
                print(f"✅ {{fixture}} carregado com sucesso")
            except Exception as e:
                print(f"⚠️ {{fixture}}: {{e}}")
        else:
            print(f"ℹ️ {{fixture}}: arquivo não encontrado")
    
    print("🎉 Restauração concluída!")

if __name__ == "__main__":
    main()
"""
    
    script_path = "restaurar_dados_mysql.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"📝 Script de restauração criado: {script_path}")

def main():
    """Função principal"""
    print("💾 Backup do SQLite - Encanto Íntimo")
    print("=" * 40)
    
    # Verificar se SQLite existe
    if not verificar_sqlite():
        return
    
    # Configurar Django
    configurar_django()
    
    # Criar backup do arquivo
    if not criar_backup_arquivo():
        return
    
    # Exportar dados
    backup_dir = exportar_dados()
    if not backup_dir:
        return
    
    # Criar script de restauração
    criar_script_restauracao(backup_dir)
    
    print("\n🎉 Backup concluído com sucesso!")
    print("\n📋 Arquivos criados:")
    print(f"- backup_sqlite_*.db (cópia do banco)")
    print(f"- {backup_dir}/ (dados em JSON)")
    print("- restaurar_dados_mysql.py (script de restauração)")
    
    print("\n⚠️ IMPORTANTE:")
    print("Execute o backup ANTES de alterar para MySQL!")

if __name__ == "__main__":
    main()
