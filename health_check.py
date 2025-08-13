"""
Script para verificar a saúde do projeto Encanto Íntimo
Executa verificações de configuração, dependências e funcionalidades.
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'encanto_intimo.settings.dev')
django.setup()

from django.core.management import call_command
from django.db import connection
from django.conf import settings
from django.test.utils import get_runner
from django.contrib.auth import get_user_model

def check_database():
    """Verifica conexão com o banco de dados"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Conexão com banco de dados: OK")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

def check_migrations():
    """Verifica se há migrações pendentes"""
    try:
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print(f"⚠️  Há {len(plan)} migrações pendentes")
            for migration in plan:
                print(f"   - {migration[0]}.{migration[1]}")
            return False
        else:
            print("✅ Migrações: Todas aplicadas")
            return True
    except Exception as e:
        print(f"❌ Erro ao verificar migrações: {e}")
        return False

def check_static_files():
    """Verifica configuração de arquivos estáticos"""
    static_root = getattr(settings, 'STATIC_ROOT', None)
    
    if static_root and Path(static_root).exists():
        print("✅ Arquivos estáticos: Coletados")
        return True
    else:
        print("⚠️  Arquivos estáticos: Não coletados (execute collectstatic)")
        return False

def check_media_files():
    """Verifica configuração de arquivos de mídia"""
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    
    if media_root:
        media_path = Path(media_root)
        if not media_path.exists():
            media_path.mkdir(parents=True, exist_ok=True)
            print("✅ Diretório de mídia: Criado")
        else:
            print("✅ Diretório de mídia: OK")
        return True
    else:
        print("❌ MEDIA_ROOT não configurado")
        return False

def check_superuser():
    """Verifica se existe um superusuário"""
    User = get_user_model()
    
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superusuário: Existe")
        return True
    else:
        print("⚠️  Superusuário: Não encontrado")
        print("   Execute: python manage.py createsuperuser")
        return False

def check_environment_variables():
    """Verifica variáveis de ambiente importantes"""
    required_vars = ['SECRET_KEY']
    optional_vars = ['DEBUG', 'ALLOWED_HOSTS']
    
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Variáveis obrigatórias faltando: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Variáveis de ambiente: OK")
        
        # Verificar opcionais
        for var in optional_vars:
            value = os.getenv(var, 'Não definida')
            print(f"   {var}: {value}")
        
        return True

def check_apps():
    """Verifica se todos os apps estão funcionando"""
    from django.apps import apps
    
    app_names = [
        'usuarios',
        'produtos',
        'pedidos',
        'carrinho',
        'pagamentos',
        'adminpanel'
    ]
    
    all_ok = True
    
    for app_name in app_names:
        try:
            app = apps.get_app_config(app_name)
            print(f"✅ App '{app_name}': OK")
        except Exception as e:
            print(f"❌ App '{app_name}': {e}")
            all_ok = False
    
    return all_ok

def check_urls():
    """Verifica configuração de URLs"""
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        # Verificar URLs principais
        important_urls = [
            'admin/',
            'usuarios/',
            'produtos/',
            'carrinho/',
            'pedidos/',
            'pagamentos/',
            'adminpanel/'
        ]
        
        url_patterns = [str(pattern.pattern) for pattern in resolver.url_patterns]
        
        missing_urls = []
        for url in important_urls:
            if not any(url.rstrip('/') in pattern for pattern in url_patterns):
                missing_urls.append(url)
        
        if missing_urls:
            print(f"⚠️  URLs possivelmente ausentes: {', '.join(missing_urls)}")
        else:
            print("✅ Configuração de URLs: OK")
        
        return len(missing_urls) == 0
        
    except Exception as e:
        print(f"❌ Erro ao verificar URLs: {e}")
        return False

def run_health_check():
    """Executa todas as verificações"""
    print("🔍 VERIFICAÇÃO DE SAÚDE DO PROJETO")
    print("=" * 50)
    
    checks = [
        ("Variáveis de Ambiente", check_environment_variables),
        ("Banco de Dados", check_database),
        ("Migrações", check_migrations),
        ("Apps Django", check_apps),
        ("URLs", check_urls),
        ("Arquivos Estáticos", check_static_files),
        ("Arquivos de Mídia", check_media_files),
        ("Superusuário", check_superuser),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            results.append((check_name, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{check_name:.<30} {status}")
    
    print(f"\n🎯 Score: {passed}/{total} verificações passaram")
    
    if passed == total:
        print("🎉 Projeto está saudável!")
        return True
    else:
        print("⚠️  Há problemas que precisam de atenção")
        return False

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == '--fix':
        print("🔧 Modo de correção automática ativado")
        
        # Tentar corrigir problemas comuns
        print("\n🔄 Aplicando migrações...")
        call_command('migrate', verbosity=0)
        
        print("🔄 Coletando arquivos estáticos...")
        call_command('collectstatic', interactive=False, verbosity=0)
        
        print("✅ Correções aplicadas\n")
    
    success = run_health_check()
    
    if not success:
        print("\n💡 Dicas:")
        print("- Execute 'python health_check.py --fix' para correções automáticas")
        print("- Consulte CONFIGURACOES.md para configuração detalhada")
        print("- Verifique o arquivo .env")
        
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
