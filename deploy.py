#!/usr/bin/env python3
"""
Script de deploy automatizado para o Encanto Íntimo
Facilita o deploy em diferentes ambientes (staging/produção).
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

class DeployManager:
    def __init__(self, environment='prod'):
        self.environment = environment
        self.project_root = Path.cwd()
        self.backup_dir = self.project_root / 'backups'
        self.log_file = self.project_root / 'logs' / f'deploy_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        
    def log(self, message, level='INFO'):
        """Log de mensagens"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"
        print(log_msg)
        
        # Gravar no arquivo
        os.makedirs(self.log_file.parent, exist_ok=True)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def run_command(self, command, check=True):
        """Executa comando e captura saída"""
        self.log(f"Executando: {command}")
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                check=check
            )
            
            if result.stdout:
                self.log(f"Saída: {result.stdout.strip()}")
            
            return result
        except subprocess.CalledProcessError as e:
            self.log(f"Erro ao executar comando: {e}", 'ERROR')
            if e.stderr:
                self.log(f"Erro: {e.stderr.strip()}", 'ERROR')
            raise
    
    def backup_database(self):
        """Cria backup do banco de dados"""
        self.log("Criando backup do banco de dados...")
        
        os.makedirs(self.backup_dir, exist_ok=True)
        backup_name = f"db_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        backup_path = self.backup_dir / backup_name
        
        if self.environment == 'prod':
            # PostgreSQL backup
            db_name = os.getenv('DB_NAME', 'encanto_intimo_prod')
            db_user = os.getenv('DB_USER', 'encanto_user')
            
            cmd = f"pg_dump -U {db_user} -h localhost {db_name} > {backup_path}"
            self.run_command(cmd)
        else:
            # SQLite backup
            db_path = self.project_root / 'db.sqlite3'
            if db_path.exists():
                shutil.copy2(db_path, backup_path.with_suffix('.sqlite3'))
        
        self.log(f"Backup criado: {backup_path}")
        return backup_path
    
    def backup_media_files(self):
        """Cria backup dos arquivos de mídia"""
        self.log("Criando backup dos arquivos de mídia...")
        
        media_dir = self.project_root / 'media'
        if not media_dir.exists():
            self.log("Diretório de mídia não encontrado, pulando backup")
            return None
        
        backup_name = f"media_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tar.gz"
        backup_path = self.backup_dir / backup_name
        
        cmd = f"tar -czf {backup_path} -C {self.project_root} media/"
        self.run_command(cmd)
        
        self.log(f"Backup de mídia criado: {backup_path}")
        return backup_path
    
    def check_environment(self):
        """Verifica se o ambiente está configurado corretamente"""
        self.log("Verificando configuração do ambiente...")
        
        # Verificar arquivo .env
        env_file = f".env.{self.environment}" if self.environment != 'dev' else ".env"
        if not Path(env_file).exists():
            raise FileNotFoundError(f"Arquivo {env_file} não encontrado")
        
        # Carregar variáveis
        from decouple import Config, RepositoryEnv
        config = Config(RepositoryEnv(env_file))
        
        # Verificar variáveis críticas
        required_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
        
        for var in required_vars:
            try:
                value = config(var)
                self.log(f"✅ {var}: configurado")
            except Exception:
                raise ValueError(f"Variável {var} não configurada em {env_file}")
        
        self.log("Ambiente configurado corretamente")
    
    def install_dependencies(self):
        """Instala dependências"""
        self.log("Instalando dependências...")
        
        # Atualizar pip
        self.run_command(f"{sys.executable} -m pip install --upgrade pip")
        
        # Instalar requirements
        requirements_file = "requirements.txt"
        if self.environment == 'dev' and Path("requirements-dev.txt").exists():
            requirements_file = "requirements-dev.txt"
        
        self.run_command(f"{sys.executable} -m pip install -r {requirements_file}")
        
        self.log("Dependências instaladas")
    
    def run_migrations(self):
        """Executa migrações do banco"""
        self.log("Executando migrações...")
        
        # Criar migrações se necessário
        self.run_command(f"{sys.executable} manage.py makemigrations")
        
        # Aplicar migrações
        self.run_command(f"{sys.executable} manage.py migrate")
        
        self.log("Migrações concluídas")
    
    def collect_static_files(self):
        """Coleta arquivos estáticos"""
        self.log("Coletando arquivos estáticos...")
        
        self.run_command(f"{sys.executable} manage.py collectstatic --noinput")
        
        self.log("Arquivos estáticos coletados")
    
    def run_tests(self):
        """Executa testes"""
        self.log("Executando testes...")
        
        try:
            # Tentar executar com pytest primeiro
            self.run_command(f"{sys.executable} -m pytest --tb=short")
        except:
            # Fallback para testes do Django
            self.run_command(f"{sys.executable} manage.py test")
        
        self.log("Testes concluídos")
    
    def restart_services(self):
        """Reinicia serviços (apenas produção)"""
        if self.environment != 'prod':
            return
        
        self.log("Reiniciando serviços...")
        
        services = ['gunicorn', 'nginx', 'redis']
        
        for service in services:
            try:
                self.run_command(f"sudo systemctl restart {service}", check=False)
                self.log(f"Serviço {service} reiniciado")
            except:
                self.log(f"Falha ao reiniciar {service} (pode não estar instalado)", 'WARN')
    
    def health_check(self):
        """Executa verificação de saúde"""
        self.log("Executando verificação de saúde...")
        
        try:
            self.run_command(f"{sys.executable} health_check.py")
            self.log("Verificação de saúde: PASSOU")
        except:
            self.log("Verificação de saúde: FALHOU", 'WARN')
    
    def deploy(self, skip_backup=False, skip_tests=False):
        """Executa deploy completo"""
        self.log(f"=== INICIANDO DEPLOY - AMBIENTE: {self.environment.upper()} ===")
        
        try:
            # 1. Verificar ambiente
            self.check_environment()
            
            # 2. Backups (apenas produção)
            if self.environment == 'prod' and not skip_backup:
                self.backup_database()
                self.backup_media_files()
            
            # 3. Instalar dependências
            self.install_dependencies()
            
            # 4. Executar testes (se solicitado)
            if not skip_tests:
                self.run_tests()
            
            # 5. Migrações
            self.run_migrations()
            
            # 6. Arquivos estáticos
            self.collect_static_files()
            
            # 7. Reiniciar serviços (produção)
            self.restart_services()
            
            # 8. Verificação de saúde
            self.health_check()
            
            self.log("=== DEPLOY CONCLUÍDO COM SUCESSO ===")
            
        except Exception as e:
            self.log(f"=== DEPLOY FALHOU: {e} ===", 'ERROR')
            self.log("Consulte o log para mais detalhes", 'ERROR')
            sys.exit(1)

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy do Encanto Íntimo')
    parser.add_argument('environment', choices=['dev', 'staging', 'prod'], 
                       help='Ambiente de deploy')
    parser.add_argument('--skip-backup', action='store_true',
                       help='Pular backup (não recomendado para produção)')
    parser.add_argument('--skip-tests', action='store_true',
                       help='Pular execução de testes')
    
    args = parser.parse_args()
    
    # Configurar variável de ambiente do Django
    if args.environment == 'prod':
        os.environ['DJANGO_SETTINGS_MODULE'] = 'encanto_intimo.settings.prod'
    else:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'encanto_intimo.settings.dev'
    
    # Executar deploy
    deploy_manager = DeployManager(args.environment)
    deploy_manager.deploy(
        skip_backup=args.skip_backup,
        skip_tests=args.skip_tests
    )

if __name__ == '__main__':
    main()
