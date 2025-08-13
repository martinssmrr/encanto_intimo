# 🐬 Migração do SQLite para MySQL - Encanto Íntimo

## 📋 Requisitos Implementados

### ✅ Configurações de Banco
- **Nome:** `db_encanto`
- **Usuário:** `encanto_admin`
- **Senha:** `Marrequeiro3750@` (configurada no .env)
- **Host:** `localhost` (configurável para produção)
- **Porta:** `3306`
- **Engine:** `django.db.backends.mysql`

### ✅ Segurança
- Credenciais armazenadas no `.env` usando `python-decouple`
- Configurações específicas por ambiente (dev/prod)
- SSL habilitado em produção

---

## 🚀 Como Executar a Migração

### **Passo 1: Instalar Dependências**

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar mysqlclient e dependências
pip install -r requirements.txt
```

**⚠️ Possíveis problemas no Windows:**
- Se houver erro com `mysqlclient`, instale o Visual C++ Build Tools
- Alternativa: `pip install mysqlclient --find-links https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient`

### **Passo 2: Configurar MySQL Server**

```sql
-- Conectar como root no MySQL
mysql -u root -p

-- Verificar se funciona (opcional - será feito pelo script)
CREATE DATABASE IF NOT EXISTS db_encanto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'encanto_admin'@'localhost' IDENTIFIED BY 'Marrequeiro3750@';
GRANT ALL PRIVILEGES ON db_encanto.* TO 'encanto_admin'@'localhost';
FLUSH PRIVILEGES;
```

### **Passo 3: Fazer Backup do SQLite (IMPORTANTE!)**

```bash
# Fazer backup dos dados existentes
python backup_sqlite.py
```

**Arquivos gerados:**
- `backup_sqlite_YYYYMMDD_HHMMSS.db` - Cópia do banco SQLite
- `backup_data_YYYYMMDD_HHMMSS/` - Dados em formato JSON
- `restaurar_dados_mysql.py` - Script para restaurar dados

### **Passo 4: Configurar MySQL**

```bash
# Executar configuração automatizada
python setup_mysql.py
```

**O que o script faz:**
1. Testa conexão com MySQL
2. Cria banco `db_encanto`
3. Cria usuário `encanto_admin`
4. Configura privilégios
5. Testa conexão Django
6. Executa migrações

### **Passo 5: Aplicar Migrações**

```bash
# Se o script anterior funcionou, pule este passo
# Caso contrário, execute manualmente:

python manage.py migrate --settings=encanto_intimo.settings.dev
```

### **Passo 6: Restaurar Dados (Se houver)**

```bash
# Se você tinha dados no SQLite, restaure:
python restaurar_dados_mysql.py
```

### **Passo 7: Criar Superusuário**

```bash
python manage.py createsuperuser --settings=encanto_intimo.settings.dev
```

### **Passo 8: Testar**

```bash
python manage.py runserver --settings=encanto_intimo.settings.dev
```

---

## ⚙️ Configurações Implementadas

### **Base Settings (`base.py`)**
```python
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.mysql'),
        'NAME': config('DB_NAME', default='db_encanto'),
        'USER': config('DB_USER', default='encanto_admin'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'STRICT_TRANS_TABLES',
            'init_command': "SET innodb_strict_mode=1",
        },
        'CONN_MAX_AGE': 60,
        'CONN_HEALTH_CHECKS': True,
    }
}
```

### **Desenvolvimento (`dev.py`)**
- MySQL local
- Conexões de 60 segundos
- SSL desabilitado

### **Produção (`prod.py`)**
- MySQL com SSL
- Conexões de 300 segundos
- Configurações otimizadas

### **Variáveis de Ambiente (`.env`)**
```env
# === MYSQL DATABASE ===
DB_ENGINE=django.db.backends.mysql
DB_NAME=db_encanto
DB_USER=encanto_admin
DB_PASSWORD=Marrequeiro3750@
DB_HOST=localhost
DB_PORT=3306
```

---

## 🔧 Otimizações MySQL Implementadas

### **Charset e Collation**
- `utf8mb4` para suporte completo Unicode (emojis, etc.)
- `utf8mb4_unicode_ci` para comparações

### **Configurações InnoDB**
- `innodb_strict_mode=1` - Validação rigorosa
- `STRICT_TRANS_TABLES` - SQL mode restritivo

### **Connection Pooling**
- `CONN_MAX_AGE` configurado por ambiente
- `CONN_HEALTH_CHECKS` habilitado

---

## 🛡️ Segurança

### **Produção**
- SSL obrigatório
- Variáveis de ambiente para todas as credenciais
- Validação de configurações

### **Desenvolvimento**
- SSL opcional
- Mesmas práticas de segurança
- Fácil configuração local

---

## 🔍 Troubleshooting

### **Erro: "No module named 'MySQLdb'"**
```bash
pip install mysqlclient
```

### **Erro: Microsoft Visual C++ 14.0 is required**
1. Instalar Visual Studio Build Tools
2. Ou usar wheel pré-compilado:
```bash
pip install mysqlclient --find-links https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
```

### **Erro: "Access denied for user"**
- Verificar se MySQL está rodando
- Verificar credenciais no `.env`
- Executar como administrador se necessário

### **Erro: "Can't connect to MySQL server"**
- Verificar se MySQL está rodando: `net start mysql`
- Verificar porta 3306: `netstat -an | findstr 3306`

### **Erro de charset/encoding**
- Verificar se banco foi criado com `utf8mb4`
- Recriar banco se necessário:
```sql
DROP DATABASE db_encanto;
CREATE DATABASE db_encanto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## ✅ Validação Final

### **Checklist Pós-Migração**

- [ ] MySQL Server rodando
- [ ] Banco `db_encanto` criado
- [ ] Usuário `encanto_admin` configurado
- [ ] Migrações aplicadas sem erro
- [ ] Django conecta ao MySQL
- [ ] Dados restaurados (se aplicável)
- [ ] Superusuário criado
- [ ] Interface admin acessível
- [ ] Aplicação roda sem erros

### **Comandos de Verificação**

```bash
# Testar conexão
python manage.py dbshell --settings=encanto_intimo.settings.dev

# Verificar migrações
python manage.py showmigrations --settings=encanto_intimo.settings.dev

# Verificar modelos
python manage.py check --settings=encanto_intimo.settings.dev
```

---

## 📊 Performance MySQL vs SQLite

### **Vantagens do MySQL**
- ✅ Melhor performance em produção
- ✅ Suporte a múltiplas conexões simultâneas
- ✅ Backup e replicação robustos
- ✅ Recursos avançados (views, procedures, etc.)
- ✅ Melhor para aplicações com múltiplos usuários

### **Configurações de Performance**
- Connection pooling configurado
- Charset otimizado (utf8mb4)
- SQL mode rigoroso
- Health checks habilitados

---

## 🎯 Próximos Passos

1. **Monitoramento:** Implementar logs de performance do banco
2. **Backup:** Configurar backup automático em produção
3. **Otimização:** Analisar queries lentas com `django-debug-toolbar`
4. **Índices:** Revisar e otimizar índices das tabelas
5. **Cache:** Implementar cache Redis para consultas frequentes

**🎉 Migração MySQL implementada com sucesso!**
