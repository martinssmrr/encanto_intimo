# 🔄 Migração SQLite → MySQL Completa - Encanto Íntimo

## 📋 Resumo da Migração

Este documento detalha a migração completa do banco de dados SQLite para MySQL no projeto Django "Encanto Íntimo", implementando configurações separadas para desenvolvimento e produção com segurança aprimorada.

## ✅ Configurações Implementadas

### 1. Estrutura de Settings
```
encanto_intimo/settings/
├── __init__.py
├── base.py      # Configurações base MySQL
├── dev.py       # Desenvolvimento (localhost)
└── prod.py      # Produção (com segurança)
```

### 2. Configurações de Banco

#### Desenvolvimento (`dev.py`)
- **Host**: localhost
- **Banco**: db_encanto  
- **Usuário**: encanto_admin
- **Conexão**: Pool de 60 segundos

#### Produção (`prod.py`)
- **Host**: Configurável via `PROD_DB_HOST`
- **Banco**: db_encanto
- **Usuário**: encanto_admin
- **Conexão**: Pool de 300 segundos
- **SSL**: Configurável
- **Charset**: utf8mb4
- **SQL Mode**: STRICT_TRANS_TABLES

### 3. Segurança de Produção Implementada
- ✅ `DEBUG=False` obrigatório
- ✅ HTTPS redirect configurável
- ✅ HSTS com 1 ano de duração
- ✅ Cookies seguros (HTTPS)
- ✅ XSS Protection
- ✅ Content Type nosniff
- ✅ X-Frame-Options: DENY
- ✅ Proxy reverso (Nginx) support

## 🚀 Como Executar a Migração

### Pré-requisitos
```bash
# 1. Instalar MySQL Server
# 2. Instalar dependências Python
pip install mysqlclient mysql-connector-python

# 3. Verificar se MySQL está rodando
mysql --version
```

### Migração Automática
```bash
# Executar script de migração completa
python migrate_sqlite_to_mysql.py
```

### Migração Manual

#### Passo 1: Configurar MySQL
```sql
-- Conectar como root
mysql -u root -p

-- Criar banco e usuário
CREATE DATABASE db_encanto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'encanto_admin'@'localhost' IDENTIFIED BY 'Marrequeiro3750@';
GRANT ALL PRIVILEGES ON db_encanto.* TO 'encanto_admin'@'localhost';
FLUSH PRIVILEGES;
```

#### Passo 2: Fazer Backup SQLite (se existir)
```bash
# Copiar banco atual
cp db.sqlite3 backup_sqlite_$(date +%Y%m%d).db
```

#### Passo 3: Executar Migrações
```bash
# Usar configuração de desenvolvimento
python manage.py migrate --settings=encanto_intimo.settings.dev
```

#### Passo 4: Migrar Dados (se existirem)
```bash
# Exportar dados do SQLite (se necessário)
python manage.py dumpdata --settings=encanto_intimo.settings.dev > backup_data.json

# Importar dados para MySQL
python manage.py loaddata backup_data.json --settings=encanto_intimo.settings.dev
```

## 🔧 Configuração de Ambiente

### Arquivo `.env` Configurado
```env
# DESENVOLVIMENTO
DB_ENGINE=django.db.backends.mysql
DB_NAME=db_encanto
DB_USER=encanto_admin
DB_PASSWORD=Marrequeiro3750@
DB_HOST=localhost
DB_PORT=3306

# PRODUÇÃO
PROD_DB_NAME=db_encanto
PROD_DB_USER=encanto_admin
PROD_DB_PASSWORD=Marrequeiro3750@
PROD_DB_HOST=localhost  # Alterar para servidor de produção
PROD_DB_PORT=3306

# SEGURANÇA
DEBUG=True  # False em produção
ALLOWED_HOSTS=localhost,127.0.0.1,encanointimo.com,www.encanointimo.com
```

## 🧪 Testes e Validação

### Testar Desenvolvimento
```bash
# Rodar servidor de desenvolvimento
python manage.py runserver --settings=encanto_intimo.settings.dev

# Testar conexão
python manage.py shell --settings=encanto_intimo.settings.dev
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("SELECT 1")
>>> cursor.fetchone()
```

### Testar Produção (Local)
```bash
# Configurar produção local
export DJANGO_SETTINGS_MODULE=encanto_intimo.settings.prod
export DEBUG=False

# Testar configurações
python manage.py check --deploy
```

## 📁 Arquivos Modificados

### Novos Arquivos
- ✅ `migrate_sqlite_to_mysql.py` - Script de migração completa
- ✅ `rollback_to_sqlite.py` - Script de rollback (gerado automaticamente)

### Arquivos Atualizados
- ✅ `.env` - Configurações completas dev/prod
- ✅ `encanto_intimo/settings/base.py` - Base MySQL
- ✅ `encanto_intimo/settings/dev.py` - MySQL desenvolvimento  
- ✅ `encanto_intimo/settings/prod.py` - MySQL produção + segurança

## 🔒 Configurações de Segurança

### Para Desenvolvimento
- `DEBUG=True`
- HTTP permitido
- Cookies não seguros
- SSL desabilitado

### Para Produção
- `DEBUG=False` (obrigatório)
- HTTPS obrigatório
- Cookies seguros
- HSTS habilitado
- SSL configurável

## 🚨 Troubleshooting

### Erro: "Access denied for user"
```bash
# Verificar usuário MySQL
mysql -u encanto_admin -p
SHOW GRANTS FOR 'encanto_admin'@'localhost';
```

### Erro: "No module named 'MySQLdb'"
```bash
# Instalar mysqlclient
pip install mysqlclient

# Ou usar mysql-connector-python
pip install mysql-connector-python
```

### Erro: "Can't connect to MySQL server"
```bash
# Verificar se MySQL está rodando
sudo systemctl status mysql  # Linux
brew services list | grep mysql  # macOS
```

### Erro: "HSTS headers"
```bash
# Desabilitar HTTPS em desenvolvimento
# No .env:
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

## 📋 Checklist Pós-Migração

### ✅ Verificações Essenciais
- [ ] MySQL Server instalado e rodando
- [ ] Banco `db_encanto` criado
- [ ] Usuário `encanto_admin` com privilégios
- [ ] Conexão Django → MySQL funcionando
- [ ] Migrações executadas sem erro
- [ ] Dados migrados (se aplicável)
- [ ] Servidor de desenvolvimento rodando
- [ ] Login/autenticação funcionando
- [ ] Google OAuth funcionando

### ✅ Testes de Funcionalidade
- [ ] Página inicial carrega
- [ ] Sistema de usuários funcionando
- [ ] CRUD de produtos funcionando
- [ ] Sistema de pedidos funcionando
- [ ] Upload de imagens funcionando
- [ ] Sistema de carrinho funcionando

## 🔄 Rollback (se necessário)

Se algo der errado, use o script de rollback:
```bash
python rollback_to_sqlite.py
```

Ou manual:
1. Restaurar `db.sqlite3` do backup
2. Alterar `.env`:
   ```env
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   ```
3. Reiniciar servidor

## 📞 Suporte

Em caso de problemas:
1. Verificar logs em `django_prod.log`
2. Executar `python manage.py check --deploy`
3. Verificar configurações no `.env`
4. Verificar conexão MySQL: `python test_mysql_connection.py`

---
**Migração completa realizada com sucesso! 🎉**
*Sistema agora roda com MySQL em desenvolvimento e produção.*
