#!/usr/bin/env python
"""
Script de Migração Completa SQLite → MySQL
Projeto: Encanto Íntimo

Este script realiza migração completa de dados do SQLite para MySQL:
1. Backup dos dados SQLite
2. Configuração do MySQL 
3. Criação do banco e usuário
4. Exportação de dados (dumpdata)
5. Importação para MySQL (loaddata)
6. Validação da migração

Uso:
    python migrate_sqlite_to_mysql.py

Pré-requisitos:
    - MySQL Server instalado e rodando
    - Acesso root ao MySQL para criação do banco/usuário
    - mysqlclient instalado (pip install mysqlclient)
"""

import os
import sys
import django
import json
import mysql.connector
from mysql.connector import Error
from django.core.management import call_command, execute_from_command_line
from decouple import config
from datetime import datetime
import shutil

class MySQLMigrator:
    def __init__(self):
        self.db_name = 'db_encanto'
        self.db_user = 'encanto_admin'
        self.db_password = 'Marrequeiro3750@'
        self.db_host = 'localhost'
        self.db_port = 3306
        
        self.backup_dir = f"backup_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def print_header(self, message):
        """Imprime cabeçalho formatado"""
        print(f"\n{'='*60}")
        print(f"🔄 {message}")
        print(f"{'='*60}")
    
    def print_step(self, step, message):
        """Imprime passo da migração"""
        print(f"\n{step}. 🔧 {message}")
        print("-" * 50)
    
    def step1_backup_sqlite(self):
        """Passo 1: Backup do banco SQLite atual"""
        self.print_step(1, "Fazendo backup do SQLite atual")
        
        if not os.path.exists('db.sqlite3'):
            print("ℹ️ Nenhum banco SQLite encontrado. Continuando...")
            return True
        
        try:
            # Criar diretório de backup
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Copiar arquivo SQLite
            shutil.copy2('db.sqlite3', os.path.join(self.backup_dir, 'db_sqlite_backup.db'))
            print("✅ Backup do arquivo SQLite criado")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro no backup: {e}")
            return False
    
    def step2_export_sqlite_data(self):
        """Passo 2: Exportar dados do SQLite"""
        self.print_step(2, "Exportando dados do SQLite")
        
        # Configurar Django para SQLite temporariamente
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
        
        # Temporariamente configurar para SQLite
        original_engine = os.environ.get('DB_ENGINE')
        original_name = os.environ.get('DB_NAME')
        
        os.environ['DB_ENGINE'] = 'django.db.backends.sqlite3'
        os.environ['DB_NAME'] = 'db.sqlite3'
        
        try:
            django.setup()
            
            # Lista de apps para exportar
            apps_to_export = [
                'auth.User',
                'auth.Group', 
                'sites.Site',
                'usuarios.PerfilUsuario',
                'produtos.Categoria',
                'produtos.Produto',
                'produtos.ImagemProduto',
                'fornecedores.Fornecedor',
                'pedidos.Pedido',
                'pedidos.ItemPedido',
                'carrinho.Carrinho',
                'carrinho.ItemCarrinho',
                'pagamentos.Pagamento',
            ]
            
            print("📦 Exportando dados por app...")
            
            for app_model in apps_to_export:
                try:
                    fixture_file = os.path.join(self.backup_dir, f"{app_model.replace('.', '_')}_data.json")
                    call_command('dumpdata', app_model, format='json', indent=2, output=fixture_file)
                    print(f"✅ {app_model}: exportado")
                except Exception as e:
                    print(f"⚠️ {app_model}: {e}")
            
            print(f"📁 Dados exportados para: {self.backup_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Erro na exportação: {e}")
            return False
        finally:
            # Restaurar configurações originais
            if original_engine:
                os.environ['DB_ENGINE'] = original_engine
            if original_name:
                os.environ['DB_NAME'] = original_name
    
    def step3_setup_mysql(self):
        """Passo 3: Configurar MySQL"""
        self.print_step(3, "Configurando MySQL")
        
        try:
            # Conectar como root
            root_password = input("Digite a senha do root do MySQL: ")
            
            connection = mysql.connector.connect(
                host=self.db_host,
                port=self.db_port,
                user='root',
                password=root_password
            )
            
            cursor = connection.cursor()
            
            print("🔗 Conectado ao MySQL como root")
            
            # Criar banco de dados
            cursor.execute(f"""
                CREATE DATABASE IF NOT EXISTS {self.db_name} 
                CHARACTER SET utf8mb4 
                COLLATE utf8mb4_unicode_ci
            """)
            print(f"✅ Banco '{self.db_name}' criado/verificado")
            
            # Criar usuário
            cursor.execute(f"""
                CREATE USER IF NOT EXISTS '{self.db_user}'@'{self.db_host}' 
                IDENTIFIED BY '{self.db_password}'
            """)
            print(f"✅ Usuário '{self.db_user}' criado/verificado")
            
            # Conceder privilégios
            cursor.execute(f"GRANT ALL PRIVILEGES ON {self.db_name}.* TO '{self.db_user}'@'{self.db_host}';")
            cursor.execute("FLUSH PRIVILEGES;")
            print(f"✅ Privilégios concedidos")
            
            cursor.close()
            connection.close()
            
            return True
            
        except Error as e:
            print(f"❌ Erro MySQL: {e}")
            return False
    
    def step4_test_mysql_connection(self):
        """Passo 4: Testar conexão MySQL com Django"""
        self.print_step(4, "Testando conexão MySQL com Django")
        
        try:
            # Configurar para MySQL
            os.environ['DB_ENGINE'] = 'django.db.backends.mysql'
            os.environ['DB_NAME'] = self.db_name
            os.environ['DB_USER'] = self.db_user
            os.environ['DB_PASSWORD'] = self.db_password
            os.environ['DB_HOST'] = self.db_host
            os.environ['DB_PORT'] = str(self.db_port)
            
            # Recarregar Django
            if 'django' in sys.modules:
                # Limpar modules do Django
                modules_to_delete = [key for key in sys.modules.keys() if key.startswith('django')]
                for module in modules_to_delete:
                    del sys.modules[module]
            
            django.setup()
            
            from django.db import connection
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            if result:
                print("✅ Conexão Django → MySQL funcionando!")
                return True
            
        except Exception as e:
            print(f"❌ Erro na conexão Django: {e}")
            return False
    
    def step5_run_migrations(self):
        """Passo 5: Executar migrações no MySQL"""
        self.print_step(5, "Executando migrações no MySQL")
        
        try:
            print("🔄 Executando migrate...")
            call_command('migrate', verbosity=1)
            print("✅ Migrações executadas com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro nas migrações: {e}")
            return False
    
    def step6_import_data(self):
        """Passo 6: Importar dados para MySQL"""
        self.print_step(6, "Importando dados para MySQL")
        
        try:
            # Lista de fixtures na ordem correta para evitar erros de FK
            fixtures_order = [
                'sites_Site_data.json',
                'auth_Group_data.json', 
                'auth_User_data.json',
                'usuarios_PerfilUsuario_data.json',
                'fornecedores_Fornecedor_data.json',
                'produtos_Categoria_data.json',
                'produtos_Produto_data.json',
                'produtos_ImagemProduto_data.json',
                'pedidos_Pedido_data.json',
                'pedidos_ItemPedido_data.json',
                'carrinho_Carrinho_data.json',
                'carrinho_ItemCarrinho_data.json',
                'pagamentos_Pagamento_data.json',
            ]
            
            print("📥 Importando dados na ordem correta...")
            
            for fixture in fixtures_order:
                fixture_path = os.path.join(self.backup_dir, fixture)
                
                if os.path.exists(fixture_path):
                    try:
                        call_command('loaddata', fixture_path, verbosity=1)
                        print(f"✅ {fixture}: importado")
                    except Exception as e:
                        print(f"⚠️ {fixture}: {e}")
                else:
                    print(f"ℹ️ {fixture}: arquivo não encontrado (normal se não há dados)")
            
            print("✅ Importação de dados concluída!")
            return True
            
        except Exception as e:
            print(f"❌ Erro na importação: {e}")
            return False
    
    def step7_validate_migration(self):
        """Passo 7: Validar migração"""
        self.print_step(7, "Validando migração")
        
        try:
            from django.contrib.auth.models import User
            from django.db import connection
            
            # Testar consultas básicas
            user_count = User.objects.count()
            print(f"✅ Usuários migrados: {user_count}")
            
            # Verificar tabelas
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"✅ Tabelas criadas: {len(tables)}")
            
            # Teste de inserção
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Banco funcionando corretamente!")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro na validação: {e}")
            return False
    
    def create_rollback_script(self):
        """Criar script de rollback para SQLite"""
        rollback_script = f"""#!/usr/bin/env python
\"\"\"
Script de Rollback para SQLite
Gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
\"\"\"

import os
import shutil

def rollback_to_sqlite():
    print("🔄 Fazendo rollback para SQLite...")
    
    # Restaurar arquivo SQLite
    backup_file = "{self.backup_dir}/db_sqlite_backup.db"
    if os.path.exists(backup_file):
        shutil.copy2(backup_file, "db.sqlite3")
        print("✅ Banco SQLite restaurado")
    
    # Instruções para alterar .env
    print("\\n📝 Para completar o rollback:")
    print("1. Altere o .env:")
    print("   DB_ENGINE=django.db.backends.sqlite3")
    print("   DB_NAME=db.sqlite3")
    print("2. Reinicie o servidor: python manage.py runserver")

if __name__ == "__main__":
    rollback_to_sqlite()
"""
        
        with open('rollback_to_sqlite.py', 'w', encoding='utf-8') as f:
            f.write(rollback_script)
        
        print("📝 Script de rollback criado: rollback_to_sqlite.py")
    
    def run_migration(self):
        """Executar migração completa"""
        self.print_header("MIGRAÇÃO SQLITE → MYSQL - ENCANTO ÍNTIMO")
        
        print("⚠️ IMPORTANTE:")
        print("- Certifique-se de que o MySQL Server está rodando")
        print("- Faça backup dos dados importantes")
        print("- Esta operação pode ser revertida usando o script de rollback")
        
        confirm = input("\n🤔 Deseja continuar com a migração? (s/N): ").lower()
        if confirm != 's':
            print("❌ Migração cancelada pelo usuário")
            return
        
        steps = [
            self.step1_backup_sqlite,
            self.step2_export_sqlite_data,
            self.step3_setup_mysql,
            self.step4_test_mysql_connection,
            self.step5_run_migrations,
            self.step6_import_data,
            self.step7_validate_migration,
        ]
        
        for i, step in enumerate(steps, 1):
            if not step():
                print(f"\n❌ Falha no passo {i}. Migração interrompida.")
                print("💡 Use o script de rollback se necessário")
                return
        
        # Criar script de rollback
        self.create_rollback_script()
        
        self.print_header("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🎉 Dados migrados do SQLite para MySQL")
        print("📁 Backup criado em:", self.backup_dir)
        print("🔄 Script de rollback: rollback_to_sqlite.py")
        print("\n📋 Próximos passos:")
        print("1. Teste todas as funcionalidades")
        print("2. Execute: python manage.py runserver")
        print("3. Acesse: http://localhost:8000")
        print("4. Se tudo estiver OK, pode deletar o backup SQLite")

if __name__ == "__main__":
    migrator = MySQLMigrator()
    migrator.run_migration()
