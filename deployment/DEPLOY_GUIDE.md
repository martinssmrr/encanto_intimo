# 🚀 GUIA DE DEPLOY - ENCANTO ÍNTIMO

Este guia abrange o deploy completo do projeto Encanto Íntimo em produção.

## 📋 Pré-requisitos

### Servidor
- Ubuntu 20.04+ ou CentOS 8+
- Mínimo: 2GB RAM, 2 CPU, 20GB disco
- Recomendado: 4GB RAM, 4 CPU, 50GB disco

### Software necessário
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Nginx
- Git

## 🔧 1. Preparação do Servidor

### 1.1. Atualizar sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2. Instalar dependências
```bash
# Pacotes básicos
sudo apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib redis-server

# Bibliotecas para Pillow
sudo apt install -y libjpeg-dev zlib1g-dev

# Ferramentas de desenvolvimento
sudo apt install -y build-essential libpq-dev
```

### 1.3. Criar usuário para aplicação
```bash
sudo adduser --system --group --shell /bin/bash encanto
sudo usermod -aG www-data encanto
```

## 🗄️ 2. Configuração do Banco de Dados

### 2.1. Configurar PostgreSQL
```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE encanto_intimo_prod;
CREATE USER encanto_user WITH PASSWORD 'SENHA_FORTE_AQUI';
GRANT ALL PRIVILEGES ON DATABASE encanto_intimo_prod TO encanto_user;
ALTER USER encanto_user CREATEDB;
\q
```

### 2.2. Configurar Redis
```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

## 📁 3. Deploy da Aplicação

### 3.1. Clonar repositório
```bash
sudo mkdir -p /var/www
sudo chown encanto:www-data /var/www
sudo -u encanto git clone https://github.com/seu-usuario/encanto-intimo.git /var/www/encanto-intimo
cd /var/www/encanto-intimo
```

### 3.2. Criar ambiente virtual
```bash
sudo -u encanto python3 -m venv venv
sudo -u encanto source venv/bin/activate
sudo -u encanto pip install --upgrade pip
sudo -u encanto pip install -r requirements.txt
```

### 3.3. Configurar variáveis de ambiente
```bash
sudo -u encanto cp .env.example .env.prod
sudo -u encanto nano .env.prod
```

Configure todas as variáveis conforme documentado no arquivo.

### 3.4. Executar setup inicial
```bash
sudo -u encanto python setup_environment.py prod
```

### 3.5. Aplicar migrações
```bash
sudo -u encanto source venv/bin/activate
export DJANGO_SETTINGS_MODULE=encanto_intimo.settings.prod
sudo -u encanto python manage.py migrate
sudo -u encanto python manage.py collectstatic --noinput
```

### 3.6. Criar superusuário
```bash
sudo -u encanto python manage.py createsuperuser
```

## 🌐 4. Configuração do Servidor Web

### 4.1. Configurar Gunicorn
```bash
# Copiar arquivos de serviço
sudo cp deployment/encanto-intimo.service /etc/systemd/system/
sudo cp deployment/encanto-intimo.socket /etc/systemd/system/

# Criar diretórios de log
sudo mkdir -p /var/log/encanto-intimo
sudo chown encanto:www-data /var/log/encanto-intimo

# Habilitar e iniciar serviços
sudo systemctl daemon-reload
sudo systemctl enable encanto-intimo.socket
sudo systemctl start encanto-intimo.socket
sudo systemctl enable encanto-intimo
sudo systemctl start encanto-intimo
```

### 4.2. Configurar Nginx
```bash
# Copiar configuração
sudo cp deployment/nginx.conf /etc/nginx/sites-available/encanto-intimo

# Habilitar site
sudo ln -s /etc/nginx/sites-available/encanto-intimo /etc/nginx/sites-enabled/

# Remover site padrão
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

## 🔒 5. Configuração SSL

### 5.1. Instalar Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 5.2. Obter certificado SSL
```bash
sudo certbot --nginx -d encantointimo.com -d www.encantointimo.com
```

### 5.3. Configurar renovação automática
```bash
sudo crontab -e
# Adicionar linha:
0 0,12 * * * python3 -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew --quiet
```

## 📊 6. Monitoramento

### 6.1. Verificar status dos serviços
```bash
sudo systemctl status encanto-intimo
sudo systemctl status nginx
sudo systemctl status postgresql
sudo systemctl status redis-server
```

### 6.2. Verificar logs
```bash
# Logs da aplicação
sudo journalctl -u encanto-intimo -f

# Logs do Nginx
sudo tail -f /var/log/nginx/encanto_intimo_error.log
sudo tail -f /var/log/nginx/encanto_intimo_access.log

# Logs do Gunicorn
sudo tail -f /var/log/encanto-intimo/gunicorn.log
```

### 6.3. Health check
```bash
cd /var/www/encanto-intimo
sudo -u encanto source venv/bin/activate
sudo -u encanto python health_check.py
```

## 🔄 7. Deploy Automatizado

### 7.1. Deploy inicial
```bash
cd /var/www/encanto-intimo
sudo -u encanto python deploy.py prod
```

### 7.2. Atualizações futuras
```bash
# Com backup
sudo -u encanto python deploy.py prod

# Sem backup (mais rápido)
sudo -u encanto python deploy.py prod --skip-backup

# Sem testes (apenas emergência)
sudo -u encanto python deploy.py prod --skip-tests
```

## 🛠️ 8. Manutenção

### 8.1. Backup manual
```bash
# Backup do banco
sudo -u postgres pg_dump encanto_intimo_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup dos arquivos de mídia
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### 8.2. Restauração
```bash
# Restaurar banco
sudo -u postgres psql encanto_intimo_prod < backup_arquivo.sql

# Restaurar mídia
tar -xzf media_backup_arquivo.tar.gz
```

### 8.3. Limpeza de logs
```bash
# Configurar logrotate
sudo nano /etc/logrotate.d/encanto-intimo
```

```
/var/log/encanto-intimo/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 encanto www-data
    postrotate
        sudo systemctl reload encanto-intimo
    endscript
}
```

## 🚨 9. Troubleshooting

### 9.1. Aplicação não inicia
```bash
# Verificar logs
sudo journalctl -u encanto-intimo --since "1 hour ago"

# Verificar configuração
sudo -u encanto python manage.py check --deploy

# Testar manualmente
sudo -u encanto python manage.py runserver 0:8000
```

### 9.2. Erro 502 (Bad Gateway)
```bash
# Verificar Gunicorn
sudo systemctl status encanto-intimo

# Verificar socket
sudo systemctl status encanto-intimo.socket

# Verificar permissões
ls -la /run/encanto-intimo/
```

### 9.3. Erro 500 (Internal Server Error)
```bash
# Verificar logs Django
sudo tail -f /var/log/encanto-intimo/gunicorn.log

# Verificar configuração
sudo -u encanto python manage.py check --deploy

# Verificar variáveis de ambiente
sudo -u encanto python -c "from decouple import config; print(config('SECRET_KEY')[:10])"
```

### 9.4. Problemas de performance
```bash
# Verificar uso de recursos
htop
df -h
free -h

# Verificar conexões Redis
redis-cli info

# Verificar conexões PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

## 📈 10. Otimizações de Performance

### 10.1. Configuração do PostgreSQL
```bash
sudo nano /etc/postgresql/13/main/postgresql.conf
```

```
# Configurações recomendadas para 4GB RAM
shared_buffers = 1GB
effective_cache_size = 3GB
maintenance_work_mem = 256MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
```

### 10.2. Configuração do Redis
```bash
sudo nano /etc/redis/redis.conf
```

```
# Configurações de memória
maxmemory 512mb
maxmemory-policy allkeys-lru

# Persistência
save 900 1
save 300 10
save 60 10000
```

### 10.3. Otimização do Nginx
```bash
sudo nano /etc/nginx/nginx.conf
```

```
worker_processes auto;
worker_connections 1024;
worker_rlimit_nofile 2048;

# Cache de arquivos
open_file_cache max=1000 inactive=20s;
open_file_cache_valid 30s;
open_file_cache_min_uses 2;
open_file_cache_errors on;
```

## ✅ 11. Checklist Final

- [ ] Servidor configurado e atualizado
- [ ] PostgreSQL e Redis funcionando
- [ ] Código clonado e dependências instaladas
- [ ] Variáveis de ambiente configuradas
- [ ] Migrações aplicadas
- [ ] Arquivos estáticos coletados
- [ ] Gunicorn configurado e rodando
- [ ] Nginx configurado e rodando
- [ ] SSL configurado (HTTPS)
- [ ] Health check passando
- [ ] Logs funcionando
- [ ] Backup configurado
- [ ] Monitoramento ativo

## 📞 Suporte

Para problemas ou dúvidas:
1. Consulte os logs detalhados
2. Execute `python health_check.py`
3. Verifique a documentação em `CONFIGURACOES.md`
4. Consulte a equipe de desenvolvimento

---
**⚠️ IMPORTANTE:** Sempre faça backup antes de deploy em produção!
